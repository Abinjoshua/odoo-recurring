# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api, _
import random
import string
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    _unique_account_id = models.Constraint(
        'UNIQUE(account_id)',
        'This email address is already registered!'
    )

    account_id = fields.Many2one('recurring.partner.account', string="Account", ondelete='cascade')
    establishment = fields.Char(string="Establishment",required=True)

    def generate_account_id(self):
        """ Function to generate the account id """
        special_characters = '!', '@', '#', '$', '%', '^', '&', '*'
        r_special_characters = random.choices(special_characters, k=2)
        r_characters = random.choices(string.ascii_letters, k=3)
        r_digits = random.choices(string.digits, k=3)
        res = r_special_characters + r_characters
        res1 = res + r_digits
        out = ''.join(res1)
        return out

    @api.model_create_multi
    def create(self, vals_list):
        """ Customer ID for the res.partner model """
        res = super().create(vals_list)
        for record in res:
            account = self.env['recurring.partner.account'].create({
                'account': self.generate_account_id(),
                'customer_id': res.id
            })
            record['account_id'] = account.id
        return res

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
