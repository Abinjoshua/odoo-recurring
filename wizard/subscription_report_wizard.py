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
        return self.env.ref(
            'recurring_subscription.action_recurring_report_subscription'
        ).report_action(self)

