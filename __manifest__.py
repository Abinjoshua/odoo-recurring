# -*- coding: utf-8 -*-
{
    'name': "Recurring Subscription",
    'version': "1.0",
    'summary': """"Recurring Subscription designed to automate billing, manage customer lifecycles, and reduce churn""",
    'description': """Recurring Subscription designed to automate billing, manage customer lifecycles, and reduce churn(description)""",
    'author': "Cybrosys",
    'website': "http://www.cybrosys.com",
    'category': 'Recurring Subscription',
    'sequence': 1,
    'application': True,
    'depends': ['base','product', 'mail','contacts'],
    'auto_install': True,
    'data':
        ["security/ir.model.access.csv",
         "views/recurring_subscription_views.xml",
         "views/recurring_subscription_credit_views.xml",
         "data/recurring_subscription_sequence.xml",
         "views/recurring_billing_schedule_views.xml",
         "views/recurring_partner_account.xml",
         "views/res_partner_views.xml",
         "views/recurring_subscription_menu_views.xml"
         ],
    'demo':['demo/subscription_product_demo.xml']
}
