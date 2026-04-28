# -*- coding: utf-8 -*-
from odoo import models, fields
import io
import json
import xlsxwriter
from odoo.tools import json_default


class CreditReportWizard(models.TransientModel):
    _name = 'credit.report.wizard'
    _description = 'Print Subscription Credit Report'

    credit_ids = fields.Many2many('recurring.subscription.credit', string='Credit')
    state = fields.Selection(
        [('pending', 'Pending'),
         ('confirmed', 'Confirmed'),
         ('first_approved', 'First approved'),
         ('fully_approved', 'Fully approved'),
         ('rejected', 'Rejected')])

    def action_print_credit_report(self):
        return self.env.ref(
            'recurring_subscription.action_subscription_credit'
        ).report_action(self)

    def action_print_xlsx_report(self):
        if self.credit_ids and self.state:
            query = """
                        SELECT id
                        FROM recurring_subscription_credit
                        WHERE id = ANY(%s)
                        AND state = %s
                    """
            params = (self.credit_ids.ids,self.state)
            self.env.cr.execute(query, params)
            row = self.env.cr.fetchall()

            ids = []
            for row in row:
                ids.append(row[0])

            docs = self.env['recurring.subscription.credit'].browse(ids)

        elif self.credit_ids:
            query = """
                        SELECT id
                        FROM recurring_subscription_credit
                        WHERE id = ANY(%s)
                    """

            params = (self.credit_ids.ids,)
            self.env.cr.execute(query, params)
            row = self.env.cr.fetchall()

            ids = []
            for row in row:
                ids.append(row[0])

            docs = self.env['recurring.subscription.credit'].browse(ids)

        elif self.state:
            query = """
                        SELECT id
                        FROM recurring_subscription_credit
                        WHERE state = %s
                    """
            params = (self.state,)
            self.env.cr.execute(query, params)
            row = self.env.cr.fetchall()
            ids = []
            for row in row:
                ids.append(row[0])

            docs = self.env['recurring.subscription.credit'].browse(ids)

        else:
            query = """
                        SELECT id 
                        FROM recurring_subscription_credit
                    """
            self.env.cr.execute(query)
            row = self.env.cr.fetchall()
            ids = []
            for row in row:
                ids.append(row[0])

            docs = self.env['recurring.subscription.credit'].browse(ids)
        names = []
        print(names)
        customers = []
        for i in docs:
            names.append(i.recurring_subscription_id.name)
            customers.append(i.partner_id.name)
        amount_applied = docs.mapped('credit_amount')
        amount_pending = docs.mapped('amount_pending')
        state = self.state

        data = {
            'customers': customers,
            'amount_applied': amount_applied,
            'amount_pending': amount_pending,
            'state': state,
            'names': names,
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'credit.report.wizard',
                     'options': json.dumps(data,
                                           default=json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Subscription Credit Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        print(self.env.user.company_id.name)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center', 'bold': True, 'shrink': True, })
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center','text_wrap': True})
        company_name = self.env.user.company_id.name
        print(type(company_name))
        sheet.merge_range('D2:K3 ', 'SUBSCRIPTION CREDIT REPORT', head)
        sheet.merge_range('G4:H5',self.env.user.company_id.name+','+self.env.user.company_id.street, txt)
        # sheet.merge_range('A2:B4',self.env.user.company_id.street, txt)
        if len(data['names']) != 1:
            print(len(data['names']))
            sheet.merge_range('D7:E7', 'Name', cell_format)
            for i, names in enumerate(data['names'],
                                      start=8):
                sheet.merge_range(f'D{i}:E{i}', names, txt)
        else:
            for i in data['names']:
                print(i)
            sheet.merge_range('A5:B5', 'Name', cell_format)
            sheet.merge_range('C5:D5', i, txt)
        sheet.merge_range('F7:G7', 'Customers', cell_format)
        for i, customer in enumerate(data['customers'],
                                     start=8):
            sheet.merge_range(f'F{i}:G{i}', customer, txt)
        sheet.merge_range('H7:I7', 'Amount Applied', cell_format)
        for i, amount_applied in enumerate(data['amount_applied'],
                                    start=8):
            sheet.merge_range(f'H{i}:I{i}', amount_applied, txt)
        sheet.merge_range('J7:K7', 'Amount Pending', cell_format)
        for i, amount_applied in enumerate(data['amount_pending'],
                                    start=8):
            sheet.merge_range(f'J{i}:K{i}', amount_applied, txt)
        if data['state']:
            sheet.merge_range('C7:D7', data['state'], txt)
            sheet.merge_range('A7:B7', 'State', cell_format)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()



