# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SubscriptionReportWizard(models.TransientModel):
    _name = 'subscription.report.wizard'
    _description = 'Print Subscription Report'

    subscription_id = fields.Many2one('recurring.subscription.credit', 'Subscription')
    recurring_intervals = fields.Selection(
        [('daily', 'Daily'),
         ('weekly', 'Weekly'),
         ('monthly', 'Monthly'),
         ('yearly', 'Yearly'), ])

    def action_print_report(self):
        data = {
            'form': self.read()[0]
        }
        print(data)
        report_action = self.env.ref('recurring_subscription.action_recurring_report_subscription').report_action(self,data=data)
        print(report_action)
        return report_action
