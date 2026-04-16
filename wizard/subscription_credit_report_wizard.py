# -*- coding: utf-8 -*-
from odoo import models, fields


class SubscriptionCreditReportWizard(models.TransientModel):
    _name = 'subscription.credit.report.wizard'
    _description = 'Print Subscription Credit Report'

    # subscription_credit_ids = fields.Many2many('recurring.subscription.credit', string='Subscription Credit')
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

class SubscriptionCreditWizardReport(models.AbstractModel):
    _name = 'report.recurring_subscription.report_sub_credit'
    _description = 'Subscription Report'

    def _get_report_values(self, docids, data=None):
        wizard = self.env['subscription.credit.report.wizard'].browse(docids)
        print(wizard)




        # domain = [
        #     ('create_date', '>=', start_date),
        #     ('create_date', '<', end_date),
        # ]

        docs = self.env['recurring.subscription.credit'].search([])
        print(docs)

        return {
            'doc_ids': docids,
            'doc_model': 'recurring.subscription.credit',
            'docs': docs,
        }
