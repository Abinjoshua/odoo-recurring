# -*- coding: utf-8 -*-
from odoo import fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    billing_schedule = fields.Char('Billing Schedule')
    credit_date = fields.Datetime('Credit Date')