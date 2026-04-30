# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Subscription(http.Controller):

    @http.route('/view/credits', type='http', auth='public', website=True)
    def view_credit(self, **kwargs):
        credits = request.env['recurring.subscription.credit'].sudo().search([])
        return request.render('recurring_subscription.portal_my_credits', {
            'credits': credits,
            'page_name': 'credits_creation'
        })

    @http.route('/edit/credits', type='http', auth='public', website=True)
    def edit_credit(self, **kwargs):
        return request.render('recurring_subscription.credits_edit_template', {})