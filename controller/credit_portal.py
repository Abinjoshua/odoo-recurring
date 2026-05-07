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

    @http.route('/edit/credits/<int:credit_id>', type='http', auth='public', website=True)
    def edit_credit(self,credit_id, **kwargs):
        credit = request.env['recurring.subscription.credit'].sudo().browse(credit_id)
        print(credit)
        subscriptions = request.env['recurring.subscription'].sudo().search([])
        return request.render('recurring_subscription.credits_edit_template', {
            'credit': credit,
            'subscriptions': subscriptions,
        })


    @http.route('/edit/credit', type='http', auth='public', website=True, methods=['POST'])
    def update_credit_form(self, **post):
        credit_id = int(post.get('credit_id'))
        credit = request.env['recurring.subscription.credit'].sudo().browse(credit_id)
        credit.write({
            'recurring_subscription_id': int(post.get('recurring_subscription_id')),
            'credit_amount': float(post.get('credit_amount')),
        })
        return request.redirect('/view/credits')

    @http.route('/delete/credit/<int:credit_id>', type='http', auth='public', website=True)
    def delete_credit(self, credit_id, **kwargs):
        subscription = request.env['recurring.subscription.credit'].sudo().browse(credit_id)
        subscription.unlink()
        return request.redirect('/view/credits')

    @http.route('/edit/confirm-credit/<int:confirm_id>', type='http', auth='user', website=True)
    def confirm_credit(self, confirm_id, **kwargs):
        credit = request.env['recurring.subscription.credit'].sudo().browse(confirm_id)
        credit.write({'state': 'confirmed'})
        return request.redirect('/view/credits')