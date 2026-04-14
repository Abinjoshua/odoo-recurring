# -*- coding: utf-8 -*-
from odoo import models, fields


class SubscriptionReportWizard(models.TransientModel):
    _name = 'subscription.report.wizard'
    _description = 'Print Subscription Report'

    subscription_ids = fields.Many2many('recurring.subscription', 'Subscription')
    recurring_intervals = fields.Selection(
        [('day', 'Day'),
         ('week', 'Week'),
         ('month', 'Month'),
         ('year', 'Year'), ])

    def action_print_report(self):
        for i in self.subscription_ids:
            data = {'subscription_ids': i.id}
            print(data)
        return self.env.ref('recurring_subscription.action_recurring_report_subscription').report_action(self, data)


class SubscriptionWizardReport(models.AbstractModel):
    _name = 'report.recurring_subscription.report_recurring_subscription'

    def _get_report_values(self,docids,data=None):
        domain = []
        if data.get('subscription_ids'):
            domain.append(('id','in',data.get('subscription_ids')))
        print(domain)
        docs = self.env['recurring.subscription'].search(domain)
        print(docs.name)
        print(data)
        return {
            'data':data,
            'doc_model':'recurring.subscription',
            'docs': docs,
        }
