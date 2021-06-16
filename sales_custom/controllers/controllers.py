# -*- coding: utf-8 -*-
from odoo import http

# class SalesCustom(http.Controller):
#     @http.route('/sales_custom/sales_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sales_custom/sales_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales_custom.listing', {
#             'root': '/sales_custom/sales_custom',
#             'objects': http.request.env['sales_custom.sales_custom'].search([]),
#         })

#     @http.route('/sales_custom/sales_custom/objects/<model("sales_custom.sales_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales_custom.object', {
#             'object': obj
#         })