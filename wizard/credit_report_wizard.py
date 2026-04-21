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
        customers = self.mapped('credit_ids.partner_id.name')
        amount_applied = self.mapped('credit_ids.credit_amount')
        amount_pending = self.mapped('credit_ids.amount_pending')
        state = self.mapped('credit_ids.state')

        data = {
            'customers': customers,
            'amount_applied': amount_applied,
            'amount_pending': amount_pending,
            'state': state
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
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center', 'bold': True, 'shrink': True, })
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        sheet.merge_range('B2:I3', 'SUBSCRIPTION CREDIT REPORT', head)
        sheet.merge_range('C7:D7', 'Customers', cell_format)
        for i, customer in enumerate(data['customers'],
                                     start=8):
            sheet.merge_range(f'C{i}:D{i}', customer, txt)
        sheet.merge_range('E7:F7', 'Amount Applied', cell_format)
        for i, amount_applied in enumerate(data['amount_applied'],
                                    start=8):
            sheet.merge_range(f'E{i}:F{i}', amount_applied, txt)
        sheet.merge_range('G7:H7', 'Amount Pending', cell_format)
        for i, amount_pending in enumerate(data['amount_pending'],
                                   start=8):
            sheet.merge_range(f'G{i}:H{i}', amount_pending, txt)
        sheet.merge_range('I7:J7', 'State', cell_format)
        for i, state in enumerate(data['state'],
                                  start=8):
            sheet.merge_range(f'I{i}:J{i}', state, txt)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()



