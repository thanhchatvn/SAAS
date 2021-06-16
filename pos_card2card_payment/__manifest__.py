# -*- coding: utf-8 -*-
###############################################################################
#
#    IATL International Pvt. Ltd.
#    Copyright (C) 2020-TODAY Tech-Receptives(<http://www.iatl-sd.com>).
#
###############################################################################
{
    'name': "pos_card2card_payment",
    'summary': """ Payment Card """,
    'description': """ When click validate payment open popup form to enter card data """,
    'author': "IATL International",
    'website': "http://www.iatl-sd.com",
    'category': 'Point Of Sale',
    'version': '0.1',
    'depends': ['point_of_sale','online_payment_api'],
    'data': [
        'views/templates.xml',
        'views/views.xml',
        ],
    # only loaded in demonstration mode
    'qweb': ['static/src/xml/*.xml'],
}