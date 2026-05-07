# -*- coding: utf-8 -*-

from odoo import http, fields, Command
from odoo.http import request


class BillingSchedulePortal(http.Controller):

    @http.route('/view/billing-schedules', type='http', auth='public', website=True)
    def view_subscription(self, **kwargs):
        billing_schedules = request.env['recurring.billing.schedule'].sudo().search([])
        return request.render('recurring_subscription.portal_my_billing_schedules', {
            'billing_schedules': billing_schedules,
            'page_name': 'billing_schedule_creation'
        })

    @http.route('/create/invoice/<int:bill_id>', type='http', auth='public', website=True)
    def create_sub_invoice(self, bill_id, **kwargs):
        # billing_schedule = request.env['recurring.billing.schedule'].sudo().browse(bill_id)
        # for record in billing_schedule:
        #     for sub in billing_schedule.recurring_subscription_ids:
        #         service_product = billing_schedule.env['product.product'].browse(83)
        #         max_cred_amount = []
        #         credit_record = billing_schedule.env['recurring.subscription.credit'].search(
        #             [('id', 'in', record.filtered_credit_ids)])
        #         for j in credit_record:
        #             max_cred_amount.append(j.credit_amount)
        #         filtered_max_cred_amount = credit_record.filtered(
        #             lambda x: x.credit_amount == max(max_cred_amount)
        #         )
        #         filtered_cred_amount = filtered_max_cred_amount.sorted(lambda x: x.create_date)
        #         cred_date = filtered_cred_amount[0].create_date
        #         cred_amount = filtered_cred_amount[0].credit_amount
        #         self.env['account.move'].create({
        #             'move_type': 'out_invoice',
        #             'partner_id': sub.customer_id.id,
        #             'billing_schedule': record.name,
        #             'invoice_date': fields.Date.today(),
        #             'credit_date': cred_date,
        #             'invoice_line_ids': [
        #                 Command.create({
        #                     'name': record.name,
        #                     'quantity': 1,
        #                     'product_id': sub.product_id.id,
        #                     'price_unit': sub.recurring_amount
        #                 }),
        #                 Command.create({
        #                     'name': f"{service_product.name} Credit date : {cred_date.strftime('%Y-%m-%d')}",
        #                     'price_unit': - cred_amount,
        #                     'quantity': 1,
        #                 })
        #             ],
        #
                # })
            # record.active = False
            return request.render('recurring_subscription.invoice_success')

    @http.route('/delete/billing-schedule/<int:bill_id>', type='http', auth='public', website=True)
    def delete_billing_schedule(self, bill_id, **kwargs):
        billing_schedule = request.env['recurring.billing.schedule'].sudo().browse(bill_id)
        billing_schedule.unlink()
        return request.redirect('/view/billing-schedules')

    @http.route('/edit/billing-schedule/<int:bill_id>', type='http', auth='public', website=True)
    def edit_billing_schedule(self, bill_id, **kwargs):
        billing_schedule = request.env['recurring.billing.schedule'].sudo().browse(bill_id)
        return request.render('recurring_subscription.billing_schedule_edit_template',{
            'billing_schedule': billing_schedule,
        })

    @http.route('/edit/billing-schedule', type='http', auth='public', website=True)
    def update_billing_schedule(self, **kwargs):
        billing_schedule_id = int(kwargs.get('billing_schedule_id'))
        billing_schedule = request.env['recurring.billing.schedule'].sudo().browse(billing_schedule_id)
        billing_schedule.write({
            'name': kwargs.get('name'),
        })
        return request.redirect('/view/billing-schedules')

