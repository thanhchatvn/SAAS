# -*- coding: utf-8 -*-
{
    'name': "sales_custom",

    'summary': """
    """,

    'description': """
        Long description of module's purpose
    """,

    'author': "IATL International",
    'website': "http://www.iatl-sd.com",
    'category': 'Sales',
    # any module necessary for this one to work correctly
    'depends': ['sale_management','sale','crm'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/res_partner_security.xml',
        'security/crm_lead_security.xml',
        'security/sale_order_security.xml',
        'views/crm_team_views.xml',
        'views/customer_views.xml',
        'views/sale_order_views.xml',
        'views/crm_views.xml',
        'views/sector.xml',
    ],
}
