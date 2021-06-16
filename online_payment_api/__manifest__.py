# -*- coding: utf-8 -*-
{
    'name': "online_payment_api",

    'summary': """
        This module is used for the online payment of 
        all the transactoins.
        """,

    'description': """
        This module is used for the online payment of 
        all the transactoins.
    """,

    'author': "AL mudather",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'API',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        'security/online_payment_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/res_config_settings.xml',
        'views/res_partner_accounting.xml',
        'views/account_jurnal_card.xml',
        'views/account_payment_custom.xml',
        'views/online_payment_server.xml',
        'wizard/cardToCardTransferWizard.xml',
        'data/account_data.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}