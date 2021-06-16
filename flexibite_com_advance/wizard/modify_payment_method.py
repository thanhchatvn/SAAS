# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from odoo import fields, models, api, _
from odoo.exceptions import Warning
from odoo.tools import float_is_zero

class wizard_pos_modify_payment(models.TransientModel):
    _name = 'wizard.pos.payment'
    _description = 'POS Payment'

    def modify_payment(self):
        payment_remove_id = self._context.get('payment_need_to_remove')
        statement_obj = self.env['account.bank.statement.line']
        payment_line_id = statement_obj.search([('id','=',payment_remove_id)])
        amount = payment_line_id.amount
        order_id = payment_line_id.pos_statement_id
        if self.journal_id.id == payment_line_id.journal_id.id:
            raise Warning("Please select different journal!")
        payment_line_id.unlink()
        self.env['pos.make.payment'].with_context({'modify_payment':True,"active_ids": [order_id.id], "active_id": order_id.id}).create({'payment_method_id': self.journal_id.id,
                                                'amount': amount}).check()

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    journal_id = fields.Many2one("account.journal",string="Journal")


class PosMakePayment(models.TransientModel):
    _inherit = 'pos.make.payment'

    
    def check(self):
        """Check the order:
        if the order is not paid: continue payment,
        if the order is paid print ticket.
        """
        self.ensure_one()
        order = self.env['pos.order'].browse(self.env.context.get('active_id', False))
        currency = order.pricelist_id.currency_id
        amount = order.amount_total - order.amount_paid
        data = self.read()[0]

        # add_payment expect a journal key
        data['journal'] = data['payment_method_id'][0]
        data['amount'] = currency.round(data['amount']) if currency else data['amount']
        # print(data,">>>>>>>>>>>>>>>>>")
        if self._context.get('modify_payment'):
            order.add_payment(data)
        if not float_is_zero(amount, precision_rounding=currency.rounding or 0.01):
            order.add_payment(data)
        if order.test_paid():
            order.action_pos_order_paid()
            return {'type': 'ir.actions.act_window_close'}
        return self.launch_payment()