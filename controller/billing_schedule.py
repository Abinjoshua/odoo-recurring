# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class BillingSchedule(http.Controller):
    @http.route('/billing-schedule', type='http', auth='user', website=True, methods=['POST'])
    def billing_schedule_page(self, **kwargs):
        recurring_subscription_ids = kwargs.getlist('recurring_subscription_ids')
        recurring_subscription_ids = list(map(int, recurring_subscription_ids)) if recurring_subscription_ids else []
        subscription_rec = request.env['recurring.subscription'].sudo().search([])
        return request.render('recurring_subscription.billing_schedule_template', {
            'subscription_rec': subscription_rec,
        })

    @http.route('/create/billing-schedule', type='http', auth='public', website=True)
    def create_subscription(self, **kwargs):
        request.env['recurring.billing.schedule'].sudo().create(kwargs)
        return request.render('recurring_subscription.billing_schedule_thanks', {})

