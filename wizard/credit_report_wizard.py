# -*- coding: utf-8 -*-
from odoo import models, fields


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



