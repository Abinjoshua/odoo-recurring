# -*- coding: utf-8 -*-
from odoo import models, fields, Command
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
    credit_ids = fields.One2many('recurring.subscription.credit', 'billing_schedule_id', string="Credits",
                                 compute='_compute_credit_ids')
    filtered_credit_ids = fields.One2many('recurring.subscription.credit', 'billing_schedule_id', string="Credits",
                                          compute="_compute_billing_schedule")
    credit_amount = fields.Monetary(string="Credit Amount", currency_field="currency_id", default=0,
                                    compute="_compute_credit_amount")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    invoice_count = fields.Integer(string="Invoice Count",default=0, compute="_compute_total_invoice_count")
    active = fields.Boolean(default=True)

    def compute_recurring_subscription_count(self):
        """ Function to get the number of recurring subscriptions """
        for record in self:
            record.recurring_subscription_count = self.env['recurring.subscription'].search_count(
                [('id', '=', record.mapped('recurring_subscription_ids.id'))])

    def action_get_recurring_subscription(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Recurring Subscription',
            'view_mode': 'list,form',
            'res_model': 'recurring.subscription',
            'domain': [('id', 'in', self.mapped('recurring_subscription_ids.id'))],
            'context': "{'create': False}"
        }
    def _compute_total_invoice_count(self):
        """ Function to get the number of recurring subscriptions """
        for record in self:
            record.invoice_count = self.env['account.move'].search_count(
                [('billing_schedule', 'in', self.name)])

    def action_get_invoices(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'view_mode': 'list,form',
            'res_model': 'account.move',
            'domain': [('billing_schedule', 'in', self.name)],
            'context': "{'create': False}"
        }

    @api.depends('recurring_subscription_ids.recurring_amount')
    def _compute_total_credit_amount(self):
        """ Function to get the total amount of credits from the recurring subscription id"""
        for record in self:
            all_cred_amount = record.mapped('recurring_subscription_ids.recurring_amount')
            record.update({'total_credit_amount': sum(all_cred_amount)})

    @api.depends('recurring_subscription_ids.customer_id')
    def _compute_total_restrict_customers(self):
        """ Function to get the customer's from the recurring subscription id"""
        for record in self:
            all_cus = record.mapped('recurring_subscription_ids.customer_id')
            record.update({'restrict_customers_ids': all_cus.mapped('id')})

    @api.depends('credit_ids.state')
    def _compute_billing_schedule(self):
        """ Function to filter the billing_schedule_ids field in the billing schedule model """
        for record in self:
            record.filtered_credit_ids = record.credit_ids.filtered(
                lambda x: x.state == 'fully_approved'
            )

    @api.depends('filtered_credit_ids.credit_amount')
    def _compute_credit_amount(self):
        for record in self:
            all_credit_amount = record.mapped('filtered_credit_ids.credit_amount')
            record.update({'credit_amount': sum(all_credit_amount)})

    @api.depends('recurring_subscription_ids')
    def _compute_credit_ids(self):
        for record in self:
            # record.mapped('recurring_subscription_ids.id')
            all_cred_ids = self.env['recurring.subscription.credit'].search(
                [('recurring_subscription_id.name', 'in', record.mapped('recurring_subscription_ids.name'))])
            record.update({'credit_ids': all_cred_ids})

    def action_create_invoice(self):
        """ Create a button in Recurring Subscription “Confirm”, when click on that button, change the state into confirmed """
        for record in self:
            for sub in self.recurring_subscription_ids:
                max_cred_amount = []
                credit_record = self.env['recurring.subscription.credit'].search([('id','in',record.filtered_credit_ids)])

                for j in credit_record:
                    max_cred_amount.append(j.credit_amount)
                    # print(max_cred_amount)
                filtered_max_cred_amount = credit_record.filtered(
                    lambda x: x.credit_amount == max(max_cred_amount)
                )
                # all_cred_amount= filtered_max_cred_amount.mapped('credit_amount')
                filtered_cred_amount = filtered_max_cred_amount.sorted(lambda x:x.create_date)
                cred_date = filtered_cred_amount[0].create_date
                cred_amount = filtered_cred_amount[0].credit_amount
                print(cred_amount)
                self.env['account.move'].create({
                    'move_type': 'out_invoice',
                    'partner_id': sub.customer_id.id,
                    'billing_schedule': record.name,
                    'invoice_date': fields.Date.today(),
                    'credit_date':cred_date,
                    'invoice_line_ids': [
                        Command.create({
                            'name': record.name,
                            'quantity': 1,
                            'product_id': sub.product_id.id,
                        }),
                        Command.create({
                            'name': record.name + ' Credit',
                            'price_unit': cred_amount,
                            'quantity': 1,
                        })
                    ],

                })
            record.active = False
