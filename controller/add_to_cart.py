# -*- coding: utf-8 -*-
from odoo import http,Command
from odoo.http import request


class AddToCart(http.Controller):
    @http.route('/cart', type='http', auth='public', website=True)
    def add_to_cart_page(self, **kwargs):
        product_rec = request.env['product.product'].sudo().search([])
        return request.render('recurring_subscription.add_to_cart_template', {
            'product_rec': product_rec,
        })

    @http.route('/add-to-cart', type='http', auth='public', website=True, methods=['GET', 'POST'])
    def create_subscription(self, **kwargs):
        website = self.env['website'].browse(1)
        print(website)
        request.env['sale.order'].sudo().create({
            'partner_id': 1,
            'state':'draft',
            'website_id': website.id,
            'team_id':2,
            'order_line': [
                Command.create({
                    'product_id': kwargs.get('product_id'),
                    'product_uom_qty': 5.0,
                    'name': 'demo',
                })]
        })
        return request.redirect('/shop/cart')




