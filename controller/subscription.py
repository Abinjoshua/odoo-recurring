# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Subscription(http.Controller):
    @http.route('/recurring-subscription', type='http', auth='public', website=True)
    def subscription_page(self, **kwargs):
        product_rec = request.env['product.product'].sudo().search([])
        return request.render('recurring_subscription.recurring_subscription_template', {
            'product_rec': product_rec,
        })

    @http.route('/create/subscription', type='http', auth='public', website=True, methods=['GET', 'POST'])
    def create_subscription(self, **kwargs):
        request.env['recurring.subscription'].sudo().create({
            'name': kwargs.get('name'),
            'product_id': int(kwargs.get('product_id')),
            'establishment':kwargs.get('establishment'),
            'recurring_amount': kwargs.get('recurring_amount'),
        })
        return request.render('recurring_subscription.subscription_thanks')

