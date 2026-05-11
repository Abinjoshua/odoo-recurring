# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class WebsiteProduct(http.Controller):
    @http.route('/get_product_categories', auth="public", type='jsonrpc',
                website=True)
    def get_product_category(self):
        """Get the website categories for the snippet."""
        public_categs = request.env[
            'recurring.subscription'].sudo().search_read(fields=['name', 'image', 'id'])
        values = {
            'categories': public_categs,
        }
        return values
