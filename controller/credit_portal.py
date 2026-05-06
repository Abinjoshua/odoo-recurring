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

    @http.route('/edit/credits/<int:sub_id>', type='http', auth='public', website=True)
    def edit_credit(self,sub_id, **kwargs):
        credit = request.env['recurring.subscription.credit'].sudo().browse(sub_id)
        print(credit)
        subscriptions = request.env['recurring.subscription'].sudo().search([])
        credit_subscription = request.env['recurring.subscription'].sudo().search([('id','=',credit.recurring_subscription_id.id)])
        return request.render('recurring_subscription.credits_edit_template', {
            'credit': credit,
            'subscriptions': subscriptions,
            'credit_subscription': credit_subscription,
        })


    @http.route('/edit/credit', type='http', auth='public', website=True)
    def update_credit_form(self, **kwargs):
        credit_id = int(kwargs.get('credit_id'))
        credit = request.env['recurring.subscription.credit'].sudo().browse(credit_id)
        credit.write({
            'recurring_subscription_id': kwargs.get('recurring_subscription_id'),
            'credit_amount': kwargs.get('credit_amount'),
        })
        return request.redirect('/view/credits')