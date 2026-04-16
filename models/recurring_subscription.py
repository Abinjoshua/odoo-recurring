# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from openpyxl.styles.builtins import total

from odoo import api
from odoo.exceptions import ValidationError
from odoo import models, fields, _, Command
import re

from odoo.orm.decorators import readonly


class RecurringSubscription(models.Model):
    _name = "recurring.subscription"
    _description = "Details of Recurring Sub"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "order desc"

    name = fields.Char(string="Name", required=True, tracking=True)
    establishment = fields.Char(string="Establishment", required=True)
    date = fields.Date(string="Date", default=fields.Date.today)
    due_date = fields.Date(default=fields.Date.today() + relativedelta(days=+15))
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
                                              string='Subscription Credits', readonly=False,
                                              compute='_compute_subscription_credit_ids')
    total_credit_applied = fields.Float(string="Total Credit Applied",compute='_compute_total_credit_applied',store=True)
    amount_pending = fields.Float(string="Amount Pending",compute='_compute_amount_pending',store=True)

    @api.depends('recurring_amount','total_credit_applied')
    def _compute_amount_pending(self):
        for record in self:
            record.amount_pending = record.recurring_amount - record.total_credit_applied

    @api.depends('subscription_credit_ids.credit_amount')
    def _compute_total_credit_applied(self):
        self.total_credit_applied = 0
        total = []
        for record in self.subscription_credit_ids:
            if record.credit_amount:
                total += record.mapped('credit_amount')
                self.total_credit_applied = sum(total)

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
                 ('recurring_subscription_id.id', '=', record.id),
                 ('period_date', '<=', record.due_date)])

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

    def action_create_invoice(self):
        """ Create a button in Recurring Subscription “Confirm”, when click on that button, change the state into confirmed """
        # if self.state == 'confirmed' and self.due_date < fields.Date.today():
        to_invoice = self.env['recurring.subscription'].search(
            [('state', '=', 'confirm'), ('due_date', '<=', fields.Date.today())])
        for record in to_invoice:
            self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': record.customer_id.id,
                'billing_schedule': record.name,
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': [
                    Command.create({
                        'name': record.name,
                        'quantity': 1,
                        'product_id': record.product_id.id,
                    }),
                    Command.create({
                        'price_unit': - record.recurring_amount,
                        'product_id': f"{record.create_date}",
                    }),
                ],

            })

    def action_done(self):
        """ Create a button in Recurring Subscription “Done”, when click on that button, change the state into done """
        self.write({'state': 'done'})
        email_values = {'email_to': self.customer_id.email}
        template = self.env.ref(
            'recurring_subscription.email_template_recurring_done')
        template.send_mail(self.id, force_send=True, email_values=email_values)
