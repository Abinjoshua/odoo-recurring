# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class WebsiteProduct(http.Controller):
    @http.route('/get_latest_credits', auth="public", type='jsonrpc',
                website=True)
    def get_latest_credits(self):
        """Get the latest credits."""
        partner = request.env.user.partner_id
        credits = request.env[
            'recurring.subscription.credit'].sudo().search_read(
            [('recurring_subscription_id.customer_id', '=', partner.id)],
            fields=['recurring_subscription_id', 'credit_amount', 'id'],order='create_date desc')
        for credit in credits:
            credit_model = request.env[
            'recurring.subscription.credit'].sudo().browse(credit['id'])
            credit['image']= credit_model.recurring_subscription_id.image
            id = str(credit['recurring_subscription_id'][0])
            link = '/edit/subscriptions/' + id
            credit['link'] = link
        values = {
            'credits': credits,
        }

        return values
