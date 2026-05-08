# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class BillingSchedule(http.Controller):
    @http.route('/billing-schedule', type='http', auth='user', website=True)
    def billing_schedule_page(self):
        subscription_rec = request.env['recurring.subscription'].sudo().search([])
        return request.render('recurring_subscription.billing_schedule_template', {
            'subscription_rec': subscription_rec,
        })

    @http.route('/create/billing-schedule', type='http', auth='public', website=True)
    def create_subscription(self, **kwargs):
        request.env['recurring.billing.schedule'].sudo().create({
            'name': kwargs.get('name'),
            'recurring_subscription_ids': request.httprequest.form.getlist('recurring_subscription_ids'),
        })
        return request.render('recurring_subscription.billing_schedule_thanks')
