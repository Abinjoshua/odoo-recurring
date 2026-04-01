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
    due_date = fields.Date(string="Date", compute='_compute_due_date')
    next_billing = fields.Date(string="Next Billing")
    is_lead = fields.Boolean(string="Lead")
    customer_id = fields.Many2one('res.partner', string="Customer", tracking=True)
    description = fields.Char(string="Description")
    terms_and_conditions = fields.Html(string="Terms and Conditions")
    product_id = fields.Many2one('product.product', string="Product", required=True, tracking=True)
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
                                              string='Subscription Credits', readonly=False, compute='_compute_subscription_credit_ids')
    # filtered_credit_ids = fields.One2many('recurring.subscription.credit', 'recurring_subscription_id',
    #                                       string='Subscription Credits', compute='_compute_filtered_credit_ids')
    # filtered_credit_amount = fields.One2many('recurring.subscription.credit', 'recurring_subscription_id',
    #                                       string='Credits Amount', compute='_compute_filtered_credit_amount')

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
                if len(z) < 2:
                    raise ValidationError("The establishment must contain at least 2 special characters")
                if len(x) < 3:
                    raise ValidationError("The establishment must contain at least 3 characters")
                if len(y) < 3:
                    raise ValidationError("The establishment must contain at least 3 digits")

    @api.depends('subscription_credit_ids.state', 'subscription_credit_ids.due_date',
                 'subscription_credit_ids.period_date')
    def _compute_subscription_credit_ids(self):
        """ Function to filter the subscription_credit_ids field in the recurring subscription model """
        for record in self:
            record.subscription_credit_ids = self.env['recurring.subscription.credit'].search(
                [('state', '=', ['fully_approved']),
                 ('recurring_subscription_id.id','=',record.id),
                 ('period_date','<=',record.due_date)])

    # @api.depends('filtered_credit_ids.recurring_amount', 'filtered_credit_ids.credit_amount')
    # def _compute_filtered_credit_amount(self):
    #     """ Function to filter the subscription_credit_ids field in the recurring subscription model """
    #     for record in self:
    #         # if record.filtered_credit_ids.recurring_amount == record.filtered_credit_ids.credit_amount:
    #         record.filtered_credit_amount = record.filtered_credit_ids.filtered(
    #             lambda rec: rec.credit_amount == rec.recurring_amount
    #         )

    @api.onchange('establishment')
    def _onchange_customer_ids(self):
        """ Function to filter the customer_ids field in the recurring subscription model """
        for record in self:
            if record.establishment:
                partner = self.env['res.partner'].search([('establishment', '=', record.establishment)])
                if partner:
                    record.customer_id = partner.id
                else:
                    raise ValidationError("Partner Not Found")

    # @api.onchange('state')
    # def _onchange_send_mail(self):
    def action_send_mail(self):
        print('working')
        for record in self:
            if record.state == 'done':
                template = self.env.ref(
                    'recurring_subscription.email_template_recurring_done')
                template.send_mail(record.id, force_send=True)
