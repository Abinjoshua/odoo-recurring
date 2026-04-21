# -*- coding: utf-8 -*-
from odoo import models, fields
import io
import json
import xlsxwriter
from odoo.tools import json_default


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
        print(self)
        return self.env.ref(
            'recurring_subscription.action_recurring_report_subscription'
        ).report_action(self)

    def action_print_xlsx_report(self):
        customers = self.mapped('subscription_ids.customer_id.name')
        names = self.mapped('subscription_ids.name')
        products = self.mapped('subscription_ids.product_id.name')
        amount = self.mapped('subscription_ids.recurring_amount')
        total_credit_applied = self.mapped('subscription_ids.total_credit_applied')
        state = self.mapped('subscription_ids.state')
        recurring_intervals = self.recurring_intervals

        data = {
            'model_id': self.id,
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
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        sheet.merge_range('B2:I3', 'SUBSCRIPTION REPORT', head)
        if data['recurring_intervals']:
            sheet.merge_range('A5:B5', 'Recurring Interval', cell_format)
            sheet.merge_range(f'C5:D5', data['recurring_intervals'], txt)
        sheet.merge_range('A7:B7', 'Name', cell_format)
        for i, name in enumerate(data['names'],
                                 start=8):
            sheet.merge_range(f'A{i}:B{i}', name, txt)
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
