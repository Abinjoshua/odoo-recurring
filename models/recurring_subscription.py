# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api
from odoo.exceptions import ValidationError
from odoo import models, fields, _
import re

class RecurringSubscription(models.Model):
    _name = "recurring.subscription"
    _description = "Details of Recurring Sub"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "order desc"

    name = fields.Char(string="Name", required=True, tracking=True)
    establishment = fields.Char(string="Establishment", required=True)
    date = fields.Date(string="Date", default=fields.Date.today)
    due_date = fields.Date(string="Due Date", compute="_compute_due_date")
    next_billing = fields.Date(string="Next Billing")
    is_lead = fields.Boolean(string="Lead")
    customer_id = fields.Many2one('res.partner', string="Customer", required=True, tracking=True)
    description = fields.Char(string="Description")
    terms_and_conditions = fields.Html(string="Terms and Conditions")
    product_id = fields.Many2one('product.template', string="Product", required=True, tracking=True)
    currency_id = fields.Many2one('res.currency', string="Currency", default=1)
    recurring_amount = fields.Monetary(string="Recurring Amount", currency_field="currency_id", required=True,
                                       default=1)
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'Done'), ('cancel', 'Cancel')], string="State",
        default='draft')
    order = fields.Char("Sequence", default=lambda self: _('New'),
                        copy=False, readonly=True, tracking=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    billing_schedule_id = fields.Many2one('recurring.billing.schedule', string="Billing Schedule")
    subscription_credit_ids = fields.One2many('recurring.subscription.credit', 'recurring_subscription_id',
                                              string='Subscription Credits', readonly=False)
    filtered_credit_ids = fields.One2many('recurring.subscription.credit', 'recurring_subscription_id',
                                          string='Subscription Credits', compute='_compute_subscription_credit_ids')

    def _compute_due_date(self):
        """ By default, the due date is set 15 days from today """
        for record in self:
            if record in self:
                record.due_date = fields.Date.today() + timedelta(days=15)

    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence for the recurring subscription model """
        for vals in vals_list:
            if vals.get('order', _('New')) == _('New'):
                vals['order'] = (self.env['ir.sequence'].
                                 next_by_code('recurring.subscription'))
        return super().create(vals_list)

    def action_confirm(self):
        """ Create a button in Recurring Subscription “Confirm”, when click on that button, change the state into confirmed """
        self.write({'state': 'confirm'})

    def action_cancel(self):
        """ Create a button in Recurring Subscription “Cancel”, when click on that button, change the state into cancel """
        self.write({'state': 'cancel'})

    @api.constrains('establishment')
    def _check_establishment(self):
        """ Validation of the establishment field 3 digits, 3 alphabets and 2 special characters """
        for record in self:
            if record in self:
                x = re.findall('[a-zA-Z]', record.establishment)
                y = re.findall('[0-9]', record.establishment)
                z = re.findall('[^a-zA-Z0-9]', record.establishment)
                print(x, y, z)
                if len(x) and len(y) < 3 and len(z) < 2:
                    raise ValidationError("The establishment must contain at least 3 alphabets and 3 digits")

    @api.depends('subscription_credit_ids.state', 'subscription_credit_ids.due_date',
                 'subscription_credit_ids.period_date')
    def _compute_subscription_credit_ids(self):
        """ Function to filter the subscription_credit_ids field in the recurring subscription model """
        for record in self:
            record.filtered_credit_ids = record.subscription_credit_ids.filtered(
                lambda i: i.state == 'fully_approved' and
                             i.period_date and
                             i.due_date and
                             i.period_date <= record.due_date
            )
