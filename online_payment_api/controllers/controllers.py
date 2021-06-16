# -*- coding: utf-8 -*-
from odoo import http

# class OnlinePaymentApi(http.Controller):
#     @http.route('/online_payment_api/online_payment_api/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/online_payment_api/online_payment_api/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('online_payment_api.listing', {
#             'root': '/online_payment_api/online_payment_api',
#             'objects': http.request.env['online_payment_api.online_payment_api'].search([]),
#         })

#     @http.route('/online_payment_api/online_payment_api/objects/<model("online_payment_api.online_payment_api"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('online_payment_api.object', {
#             'object': obj
#         })