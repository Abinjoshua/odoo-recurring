# -*- coding: utf-8 -*-
from odoo import models, fields, api
import re
from odoo.exceptions import ValidationError
from datetime import timedelta


class RecurringSubscriptionCredit(models.Model):
    _name = "recurring.subscription.credit"
    _description = "Recurring Subscription Credit"
    _rec_name = "recurring_subscription_id"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    recurring_subscription_id = fields.Many2one('recurring.subscription', string="Recurring Subscription",
                                                required=True)
    partner_id = fields.Many2one(related='recurring_subscription_id.customer_id', string="Partner")
    state = fields.Selection(
        [('pending', 'Pending'),
         ('confirmed', 'Confirmed'),
         ('first_approved', 'First approved'),
         ('fully_approved', 'Fully approved'),
         ('rejected', 'Rejected')], default='pending')
    recurring_intervals = fields.Selection(
        [('daily', 'Daily'),
         ('weekly', 'Weekly'),
         ('monthly', 'Monthly'),
         ('yearly', 'Yearly'), ])
    currency_id = fields.Many2one(related='recurring_subscription_id.currency_id', string="Currency")
    recurring_amount = fields.Monetary(related='recurring_subscription_id.recurring_amount', string="Recurring Amount",
                                       currency_field='currency_id', default=1, required=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    establishment = fields.Char(related='recurring_subscription_id.establishment', string="Establishment")
    due_date = fields.Date(string="Due Date", compute="_compute_due_date")
    credit_amount = fields.Float(string="Credit Amount", default=1)
    period_date = fields.Date(string="Period Date")
    billing_schedule_id = fields.Many2one('recurring.billing.schedule', string="Billing Schedule")

    @api.constrains('establishment')
    def _check_establishment(self):
        """ Validation of the establishment field 3 digits, 3 alphabets and 2 special characters """
        for record in self:
            x = re.findall('[a-zA-Z]', record.establishment)
            y = re.findall('[0-9]', record.establishment)
            z = re.findall('[^a-zA-Z0-9]', record.establishment)
            if (len(x) and len(y) < 3) and (len(z) < 2):
                raise ValidationError("The establishment must contain at least 3 alphabets and 3 digits")

    def _compute_due_date(self):
        """ By default, the due date is set 15 days from today """
        for record in self:
            if record in self:
                record.due_date = fields.Date.today() + timedelta(days=15)

    @api.onchange('credit_amount')
    def _onchange_credit_amount(self):
        """ The credit amount should always be lesser than the recurring amount """
        for record in self:
            if record in self:
                if record.credit_amount == 0 or record.credit_amount > record.recurring_amount:
                    record.recurring_subscription_id = None
