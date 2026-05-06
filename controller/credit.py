# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Subscription(http.Controller):
    @http.route('/credit', type='http', auth='public', website=True)
    def subscription_credit_page(self):
        subscription_rec = request.env['recurring.subscription'].sudo().search([])
        return request.render('recurring_subscription.credit_template', {
            'subscription_rec': subscription_rec,
        })

    @http.route('/create/credit', type='http', auth='public', website=True)
    def create_subscription_credit(self, **kwargs):
        request.env['recurring.subscription.credit'].sudo().create(
            {
            'recurring_subscription_id': int(kwargs.get('recurring_subscription_id')),
            'credit_amount': kwargs.get('credit_amount'),
            }
        )
        return request.redirect('/credit-created-successfully')

