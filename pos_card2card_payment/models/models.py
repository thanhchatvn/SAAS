# -*- coding: utf-8 -*-
###############################################################################
#
#    IATL International Pvt. Ltd.
#    Copyright (C) 2020-TODAY Tech-Receptives(<http://www.iatl-sd.com>).
#
###############################################################################

from odoo import models, fields, api
from odoo.addons.pos_card2card_payment.controllers import onlineTransformationPayment
from odoo.exceptions import Warning


class OnlinePosPayment(models.Model):
    _inherit = "account.journal"

    card_to_card_payment = fields.Boolean(string="card to card payment", default=False)

    inbound_payment_method_ids = fields.Many2many('account.payment.method',
                                                  'account_journal_inbound_payment_method_rel', 'journal_id',
                                                  'inbound_payment_method',
                                                  domain=[('payment_type', '=', 'inbound')],
                                                  string='For Incoming Payments',
                                                  default=lambda self: self._default_inbound_payment_methods(),
                                                  help="Manual: Get paid by cash, check or any other method outside of Odoo.\n" \
                                                       "Electronic: Get paid automatically through a payment acquirer by requesting a transaction on a card saved by the customer when buying or subscribing online (payment token).\n" \
                                                       "Batch Deposit: Encase several customer checks at once by generating a batch deposit to submit to your bank. When encoding the bank statement in Odoo,you are suggested to reconcile the transaction with the batch deposit. Enable this option from the settings.")

    
    @api.onchange('inbound_payment_method_ids','outbound_payment_method_ids')
    def make_card_payment_true(self):

        #TODO: If self.inbound_payment_method_ids or self.outbound_payment_method_ids payment card
        # not equal to card2card make the self.card_to_card_payment = False  
        if self.card_to_card_payment == True:
            self.card_to_card_payment = False

        #TODO: self.inbound_payment_method_ids payment_card code equal to card2card
        # make self.card_to_card_payment = True
        for method in self.inbound_payment_method_ids:
            if method.code == "card2card":
                self.card_to_card_payment = True
        
        #TODO: self.outbound_payment_method_ids payment_card code equal to card2card
        # make self.card_to_card_payment = True
        for method in self.outbound_payment_method_ids:
            if method.code == "card2card":
                self.card_to_card_payment = True

            
    
    
    @api.onchange('card_to_card_payment')
    def card_payment(self):
        if self.card_to_card_payment:
            returend_domain = {'domain': {'inbound_payment_method_ids': "[('payment_type','=','inbound'),('code','=', 'card2card')]"}}
            # inbound_payment_obj = self.env['account.payment.method'].search([('payment_type','=','inbound'),("code",'=', 'card2card')])
            # self.inbound_payment_method_ids = self.inbound_payment_method_ids.search([('payment_type','=','inbound'),("code",'=', 'card2card')]).id
            # self.inbound_payment_method_ids = self.inbound_payment_method_ids.browse(inbound_payment_id)
            # card_2_card_method = self.env['account.payment.method'].browse(inbound_payment_id)
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            # print(inbound_payment_obj)
            # print(inbound_payment_obj.id)
            #
            # self.inbound_payment_method_ids = inbound_payment_obj
            # print(self.inbound_payment_method_ids)
            # # for c in self.inbound_payment_method_ids:
            # #     print(c.name)
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            # return { 'value' :{'inbound_payment_method_ids' : inbound_payment_obj } }  #'domain': {'inbound_payment_method_ids': "[('payment_type','=','inbound'),('code','=', 'card2card')]"}}
            return returend_domain

        else:
            pass



class PosCardToCardTransferModel(models.Model):  # Where this wizard will appear
    # _inherit = "card.to.card.transfer.wizard"
    _name = "pos.card.to.card.transfer.model"

    # when payment type send money get From Card by default from Journal and To from partner default card ?????????

    # TODO: Add Button Transfer toAuthorization do transfer operation and after end successfully call payment post button

    @api.multi
    def transfer(self, args):
    # def transfer(self ):
        # 1) Get the Url and the Token
        pay_obj = self.env["online.payment.server"].search([], limit=1)
        
        one_line = onlineTransformationPayment.oneLinePayment()
        if pay_obj:
            # 2) Test the connection
            conn = one_line.networkIsAlive(URL=pay_obj.url, token=pay_obj.token)
            active_id = self._context.get('active_id')  # active id of the payment  with_context
            if conn:

                # 3) Send the data as Json
                respond = one_line.cardToCardTransfer(
                    URL=pay_obj.url,
                    FROM_PAN=args['from_card'],
                    toCard=args['to_card'],
                    IPIN=args['ipn'],
                    expDate=args['expiration_data'],
                    tranAmount=args['trans_amount'],
                    dynamicFees=0,
                    token=pay_obj.token)

                # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                # print(respond)
                # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

                if respond:
                    return respond