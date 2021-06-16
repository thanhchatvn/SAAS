# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.online_payment_api.controllers import onlinePayment 
from odoo.exceptions import Warning

class cardToCardTransferWizard(models.TransientModel): # Where this wizard will appear
    _name = "card.to.card.transfer.wizard"

    from_card_id = fields.Many2one('card.information', string="From Card", required=True)
    to_card_id = fields.Many2one('card.information', string="To Card", required=True)
    ipn = fields.Char(string="IPN", required=True)
    amount = fields.Char(string="Amount", compute="_get_payment_amout" ,readonly = True)
    expDate = fields.Date(string="Expiration Date", related="from_card_id.end_date")

    # when payment type send money get From Card by default from Journal and To from partner default card ?????????

    @api.one
    def _get_payment_amout(self):
        self.amount = self._context.get("apyment_amount")
        # print("################################################")
        # print(self.amount)
        # print("################################################")








    #TODO: Add Button Transfer toAuthorization do transfer operation and after end successfully call payment post button
    
    @api.multi
    def transfer(self):        
        # 1) Get the Url and the Token
        pay_obj = self.env["online.payment.server"].search([] , limit=1)
        # self.amount = self._context.get("apyment_amount")
        # print("################################################")
        # print(self.amount)
        # print("################################################")
       
        one_line = onlinePayment.oneLinePayment()
        if pay_obj:
            # 2) Test the connection
            conn = one_line.networkIsAlive(URL=pay_obj.url, token=pay_obj.token)
            active_id = self._context.get('active_id')# active id of the payment  with_context
            if conn:                     
                # 3) Get the data from wizard
                from_card = self.from_card_id.card_number
                to_card   = self.to_card_id.card_number
                ipn       = self.ipn
                amount    = self._context.get("apyment_amount")
                expDate  = str(self.expDate)
                # 4) Send the data as Json
                respond = one_line.cardToCardTransfer(
                    URL=pay_obj.url,
                    FROM_PAN=from_card,
                    toCard=to_card,
                    IPIN=ipn,
                    expDate=expDate,
                    tranAmount=amount,
                    dynamicFees=0,
                    token=pay_obj.token)
                # 5) Go and enjoy
                if respond:
                   
                    return self.env["account.payment"].browse(active_id).with_context(from_wiz = True).post()
                    