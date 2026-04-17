# -*- coding: utf-8 -*-
from odoo import models

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
            if len(docs) == 1:
                docid = docs
            else:
                docid = None

        return {
            'doc_ids': docids,
            'doc_model': 'recurring.subscription.credit',
            'docs': docs,
            'docid': docid,
            'wizard': wizard,
        }