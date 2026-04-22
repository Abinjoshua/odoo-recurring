# -*- coding: utf-8 -*-
from odoo import models, fields
import io
import json
import xlsxwriter
from odoo.tools import json_default
from datetime import datetime, timedelta


class SubscriptionReportWizard(models.TransientModel):
    _name = 'subscription.report.wizard'
    _description = 'Print Subscription Report'

    subscription_ids = fields.Many2many('recurring.subscription', 'Subscription',store=True)
    recurring_intervals = fields.Selection(
        [('day', 'Day'),
         ('week', 'Week'),
         ('month', 'Month'),
         ('year', 'Year'), ],store=True)

    def action_print_report(self):
        return self.env.ref(
            'recurring_subscription.action_recurring_report_subscription'
        ).report_action(self)

    def action_print_xlsx_report(self):
        now = datetime.now()

        if self.recurring_intervals and self.subscription_ids:
            if self.recurring_intervals == 'day':
                start_date = datetime(now.year, now.month, now.day)
                end_date = start_date + timedelta(days=1)

            elif self.recurring_intervals == 'week':
                start_date = datetime(now.year, now.month, now.day - 7)
                end_date = start_date + timedelta(now.day)

            elif self.recurring_intervals == 'month':
                start_date = datetime(now.year, now.month, 1)
                if now.month == 12:
                    end_date = datetime(now.year + 1, 1, 1)
                else:
                    end_date = datetime(now.year, now.month + 1, 1)

            elif self.recurring_intervals == 'year':
                start_date = datetime(now.year, 1, 1)
                end_date = datetime(now.year + 1, 1, 1)

            query = """
                        SELECT id
                        FROM recurring_subscription
                        WHERE create_date >= %s
                        AND create_date < %s
                        AND id = ANY(%s)
                    """

            params = (start_date, end_date, self.subscription_ids.ids)
            self.env.cr.execute(query, params)
            row = self.env.cr.fetchall()
            ids = []
            for row in row:
                ids.append(row[0])

            docs = self.env['recurring.subscription'].browse(ids)
            print(docs)

        elif self.recurring_intervals:
            if self.recurring_intervals == 'day':
                start_date = datetime(now.year, now.month, now.day)
                end_date = start_date + timedelta(days=1)

            elif self.recurring_intervals == 'week':
                start_date = datetime(now.year, now.month, now.day - 7)
                end_date = start_date + timedelta(now.day)

            elif self.recurring_intervals == 'month':
                start_date = datetime(now.year, now.month, 1)
                if now.month == 12:
                    end_date = datetime(now.year + 1, 1, 1)
                else:
                    end_date = datetime(now.year, now.month + 1, 1)

            elif self.recurring_intervals == 'year':
                start_date = datetime(now.year, 1, 1)
                end_date = datetime(now.year + 1, 1, 1)

            query = """
                        SELECT id
                        FROM recurring_subscription
                        WHERE create_date >= %s
                        AND create_date < %s
                     """
            params = (start_date, end_date)
            self.env.cr.execute(query, params)
            row = self.env.cr.fetchall()

            ids = []
            for row in row:
                ids.append(row[0])

            docs = self.env['recurring.subscription'].browse(ids)

        elif self.subscription_ids:

            query = """
                        SELECT id
                        FROM recurring_subscription
                        WHERE id = ANY(%s)
                    """

            params = (self.subscription_ids.ids,)
            self.env.cr.execute(query, params)
            row = self.env.cr.fetchall()

            ids = []
            for row in row:
                ids.append(row[0])

            docs = self.env['recurring.subscription'].browse(ids)

        else:
            query = """
                        SELECT id
                        FROM recurring_subscription
                    """
            self.env.cr.execute(query)
            row = self.env.cr.fetchall()
            ids = []
            for row in row:
                ids.append(row[0])

            docs = self.env['recurring.subscription'].browse(ids)

        customers = docs.mapped('customer_id.name')
        names = docs.mapped('name')
        products = docs.mapped('product_id.name')
        amount = docs.mapped('recurring_amount')
        total_credit_applied = docs.mapped('total_credit_applied')
        state = docs.mapped('state')
        recurring_intervals = self.recurring_intervals

        data = {
            'names': names,
            'customers': customers,
            'products': products,
            'amount': amount,
            'total_credit_applied': total_credit_applied,
            'state': state,
            'recurring_intervals': recurring_intervals,
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'subscription.report.wizard',
                     'options': json.dumps(data,
                                           default=json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Subscription Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center', 'bold': True, 'shrink': True, })
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center', 'text_wrap': True})
        sheet.merge_range('E2:I3', 'SUBSCRIPTION REPORT', head)
        sheet.merge_range('G4:H5', self.env.user.company_id.name + ',' + self.env.user.company_id.street, txt)
        if data['recurring_intervals']:
            sheet.merge_range('A5:B5', 'Recurring Interval', cell_format)
            sheet.merge_range(f'C5:D5', data['recurring_intervals'], txt)
        if len(data['names']) != 1:
            sheet.merge_range('A7:B7', 'Name', cell_format)
            for i, name in enumerate(data['names'],
                                     start=8):
                sheet.merge_range(f'A{i}:B{i}', name, txt)
        else:
            for i in data['names']:
                sheet.merge_range('A4:B4', 'Name', cell_format)
                sheet.merge_range('C4:D4', i, txt)
        sheet.merge_range('C7:D7', 'Customers', cell_format)
        for i, customer in enumerate(data['customers'],
                                     start=8):
            sheet.merge_range(f'C{i}:D{i}', customer, txt)
        sheet.merge_range('E7:F7', 'Product', cell_format)
        for i, product in enumerate(data['products'],
                                    start=8):
            sheet.merge_range(f'E{i}:F{i}', product, txt)
        sheet.merge_range('G7:H7', 'Amount', cell_format)
        for i, amount in enumerate(data['amount'],
                                   start=8):
            sheet.merge_range(f'G{i}:H{i}', amount, txt)
        sheet.merge_range('I7:J7', 'Total Credit Applied', cell_format)
        for i, total_credit_applied in enumerate(data['total_credit_applied'],
                                                 start=8):
            sheet.merge_range(f'I{i}:J{i}', total_credit_applied, txt)
        sheet.merge_range('K7:L7', 'State', cell_format)
        for i, state in enumerate(data['state'],
                                  start=8):
            sheet.merge_range(f'K{i}:L{i}', state, txt)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
