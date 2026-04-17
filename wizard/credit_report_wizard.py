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


class SubscriptionCreditWizardReport(models.AbstractModel):
    _name = 'report.recurring_subscription.report_sub_credit'
    _description = 'Subscription Report'

    def _get_report_values(self, docids, data=None):
        wizard = self.env['credit.report.wizard'].browse(docids)
        print(wizard)

        if wizard.credit_ids and wizard.state:
            domain = [
                ('id', 'in', wizard.credit_ids),
                ('state', 'in', wizard.state),
            ]
            docs = self.env['recurring.subscription.credit'].search(domain)
            if len(docs) == 1:
                docid = docs
            else:
                docid = None

        elif wizard.credit_ids:
            domain = [
                ('id', 'in', wizard.credit_ids)
            ]
            docs = self.env['recurring.subscription.credit'].search(domain)
            if len(docs) == 1:
                docid = docs
            else:
                docid = None

        elif wizard.state:
            domain = [
                ('state', 'in', wizard.state),
            ]
            docs = self.env['recurring.subscription.credit'].search(domain)
            if len(docs) == 1:
                docid = docs
            else:
                docid = None
            print(wizard.state)
        else:
            docs = self.env['recurring.subscription.credit'].search([])

        return {
            'doc_ids': docids,
            'doc_model': 'recurring.subscription.credit',
            'docs': docs,
            'docid': docid,
            'wizard': wizard,
        }
