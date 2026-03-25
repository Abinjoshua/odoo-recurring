# -*- coding: utf-8 -*-
from odoo import fields, models

class RecurringPartnerAccount(models.Model):
    _name = 'recurring.partner.account'
    _description = 'Recurring Partner Account'
    _rec_name = 'account'

    account = fields.Char(string="Account",ondelete='cascade')
    customer_id = fields.Many2one('res.partner', string="Customer",ondelete='cascade')



