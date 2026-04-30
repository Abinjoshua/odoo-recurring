# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Subscription(http.Controller):

    @http.route('/view/subscriptions', type='http', auth='public', website=True)
    def view_subscription(self, **kwargs):
        subscriptions = request.env['recurring.subscription'].sudo().search([])
        return request.render('recurring_subscription.portal_my_subscription', {
            'subscriptions': subscriptions,
            'page_name': 'subscriptions_creation'
        })

    @http.route('/edit/subscriptions', type='http', auth='public', website=True)
    def edit_subscription(self, **kwargs):
        return request.render('recurring_subscription.subscription_edit_template', {})