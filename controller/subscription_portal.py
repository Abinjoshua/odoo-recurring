# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class SubscriptionPortal(http.Controller):

    @http.route('/view/subscriptions', type='http', auth='public', website=True)
    def view_subscription(self, **kwargs):
        subscriptions = request.env['recurring.subscription'].sudo().search([])
        return request.render('recurring_subscription.portal_my_subscription', {
            'subscriptions': subscriptions,
            'page_name': 'subscriptions_creation'
        })

    @http.route('/edit/subscriptions/<int:sub_id>', type='http', auth='public', website=True)
    def edit_subscription(self,sub_id, **kwargs):
        subscription = request.env['recurring.subscription'].sudo().browse(sub_id)
        products = request.env['product.product'].sudo().search([])
        return request.render('recurring_subscription.subscription_edit_template', {
            'subscription': subscription,
            'products': products,
        })

    @http.route('/edit/subscription', type='http', auth='public', website=True)
    def update_subscription_form(self, **kwargs):
        subscription_id = int(kwargs.get('subscription_id'))
        subscription = request.env['recurring.subscription'].sudo().browse(subscription_id)
        subscription.write({
            'name': kwargs.get('name'),
            'product_id': int(kwargs.get('product_id')),
            'establishment': kwargs.get('establishment'),
            'recurring_amount': kwargs.get('recurring_amount'),
            'state': kwargs.get('state'),
        })

        return request.redirect('/view/subscriptions')

    @http.route('/delete/subscriptions/<int:sub_id>', type='http', auth='public', website=True)
    def delete_subscriptions(self,sub_id, **kwargs):
        subscription = request.env['recurring.subscription'].sudo().browse(sub_id)
        subscription.unlink()
        return request.redirect('/view/subscriptions')

    @http.route('/edit/confirm-subscription/<int:confirm_id>', type='http', auth='user', website=True)
    def confirm_subscription(self, confirm_id, **kwargs):
        subscription = request.env['recurring.subscription'].sudo().browse(confirm_id)
        subscription.write({'state': 'confirm'})
        return request.redirect('/view/subscriptions')


