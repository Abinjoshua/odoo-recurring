# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo import api


class RecurringBillingSchedule(models.Model):
    _name = "recurring.billing.schedule"
    _description = "Recurring Subscription Billing Schedule"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Billing Schedule", required=True)
    simulation = fields.Boolean(default=False)
    period = fields.Date(default=fields.Date.today, required=True)
    restrict_customers_ids = fields.Many2many('res.partner', compute='_compute_total_restrict_customers')
    active = fields.Boolean(default=True)
    recurring_subscription_ids = fields.Many2many('recurring.subscription', readonly=False, store=True)
    currency_id = fields.Many2one('res.currency', string="Currency", default=1)
    total_credit_amount = fields.Monetary(string="Total Credit Amount", currency_field="currency_id", required=True,
                                          default=0, compute="_compute_total_credit_amount")
    date_begin = fields.Datetime()
    date_end = fields.Datetime()
    recurring_subscription_count = fields.Integer(string="Recurring Subscription Count", default=0,
                                                  compute="compute_recurring_subscription_count")

    def compute_recurring_subscription_count(self):
        """ Function to get the number of recurring subscriptions """
        for record in self:
            record.recurring_subscription_count = self.env['recurring.subscription'].search_count(
                [('name', '=', record.mapped('recurring_subscription_ids.name'))])
    def action_get_recurring_subscription(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Recurring Subscription',
            'view_mode': 'list,form',
            'res_model': 'recurring.subscription',
            'domain': [('id', 'in', self.recurring_subscription_ids.id)],
            'context': "{'create': False}"
        }

    @api.depends('recurring_subscription_ids.recurring_amount')
    def _compute_total_credit_amount(self):
        for record in self:
            all_cred_amount = record.mapped('recurring_subscription_ids.recurring_amount')
            record.total_credit_amount = sum(all_cred_amount)

    @api.depends('recurring_subscription_ids.customer_id')
    def _compute_total_restrict_customers(self):
        for record in self:
            all_cus = record.mapped('recurring_subscription_ids.customer_id')
            record.restrict_customers_ids = all_cus.mapped('id')

    # @api.depends('recurring_subscription_ids.name')
    # def _compute_rec_sub(self):
    #     for record in self:
    #         all_rec = record.mapped('recurring_subscription_ids.name')
    #         record.recurring_subscription_ids = all_rec.mapped('id')
