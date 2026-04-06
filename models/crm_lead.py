# -*- coding: utf-8 -*-
from odoo import fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    order = fields.Char(string="Order")
