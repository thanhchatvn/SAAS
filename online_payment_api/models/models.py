# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.online_payment_api.controllers import onlinePayment 
from odoo.exceptions import Warning, ValidationError
# from hashlib import sha256 # this modle for password encription
from Crypto.Cipher import AES
import base64
import notify2
import os
import subprocess as notify_message


# from onlinePayment import onlinePayment
secret_key = "onlinePayment123"
cipher = AES.new(secret_key,AES.MODE_ECB)


CARD_TYPE = [
    ('partner','Partner'),
    ('owner','Owner')
]


class cardInformation(models.Model):
    _name = "card.information"
    _rec_name = "card_number"

    card_number = fields.Char(string="Card Number", required=True)
    end_date = fields.Date(string="End Date", required=True)
    default_card = fields.Boolean(string="Use this card as default")
    
    partner_id = fields.Many2one('res.partner', string="Partner")
    
    card_type = fields.Selection(CARD_TYPE, string="Card Type")

    @api.constrains("card_number")
    def card_must_be_16_digit(self):
        if len(self.card_number) != 16:
            raise ValidationError(f"Card number must be 16 number, you enter {len(self.card_number)} number(s)"  )


    

class CustomResPartner(models.Model):
    _inherit = "res.partner"


# class customResBank(models.Model):
#     _inherit = "res.bank"
#     # _inherit = "res.partner"

#     card_info_id = fields.One2many('card.information', 'partner_id', string='Card Information')

class customAccountjurnal(models.Model):
    _inherit = "res.partner.bank"
    # _inherit = "account.journal"

    card_information_id = fields.Many2one('card.information', domain="[('card_type','=','owner')]", string='Card Information')
    default_card = fields.Boolean(string="Default Card",related="card_information_id.default_card")
    
STATE = [
    ("draft","Draft"),
    ("success","Success"),
    ("failed","Failed")
]

class onlinePaymentServer(models.Model): 
    _name = "online.payment.server"  

    url = fields.Char(string="URL", required=True)
    name = fields.Char(string="Name", required=True)
    password = fields.Char(string="Password",required=True)
    token = fields.Char(string="Token", invisible= True)
    remember_me = fields.Boolean(string="Remember Me")

    state           = fields.Selection(string="State", selection=STATE, default="draft", track_visibility='onchange')
    # TODO: Add button to test The Connection
    # 1) DO the authentication first
    # 2) Test the connection with the EPS


    @api.one
    def draft_success(self):
        self.state = "success"

    @api.one
    def draft_failed(self):
        self.state = "failed"
    
    def networkIsAlive(self):
        one_line = onlinePayment.oneLinePayment()
        token = one_line.authentication(
                URL = self.url,
                username=self.name,
                password= self.password ,
                rememberMe=self.remember_me)
        self.token = token
        
        if self.token:
            try:
                conn = one_line.networkIsAlive(URL=self.url,token=self.token)

                if conn:
                    
                    notify_message.call(['notify-send','Success','The connection is established.'])
                    self.draft_success()
            except ConnectionError:
                
                notify_message.call(['notify-send','Error','check you network connection and try again!!!!! '])
                self.draft_failed()
                # raise Warning(" Connection Erro, check you network connection and try again!!!!! ") 


class OnlineAccountPayment(models.Model):
    _inherit = "account.payment"
    

    from_card_id = fields.Many2one('card.information',
                domain="[('card_type','=','partner')]", 
                string="From Card", 
                related="partner_id.bank_ids.card_information_id"
            )
    to_card_id = fields.Many2one('card.information', 
                domain="[('card_type','=','owner')]",
                string="To Card",
                related="journal_id.bank_account_id.card_information_id"
            )
    ipn = fields.Char(string="IPN")
    # sending_amount = fields.Char(string="Amount", compute="_get_payment_amout" ,readonly = True)
    sending_amount = fields.Monetary(string="Amount", compute="_get_payment_amout", readonly = True)
    expDate = fields.Date(string="Expiration Date", related="from_card_id.end_date")

    @api.onchange("amount")
    def _get_payment_amout(self):
        
        self.sending_amount = self.amount
        

    ####################################################
    #TODO:
    ###################################################
    @api.multi
    def post(self):
        if self.journal_id.type == "bank" and (self.payment_method_code == "card2card" and self.state == "draft"):
            finished = self.transfer()
            # print(finished)
            if finished["ok"]:
                
                notify_message.call(['notify-send','Success',finished["message"]])
                
                return super(OnlineAccountPayment, self).post()
            else:
                
                notify_message.call(['notify-send','Error',finished["message"]])
                
        else:
            return super(OnlineAccountPayment, self).post()

    ######################################
    #TODO: Send the money using the card#
    ####################################
    @api.multi
    def transfer(self):        
        # 1) Get the Url and the Token
        pay_obj = self.env["online.payment.server"].search([] , limit=1)
        
        one_line = onlinePayment.oneLinePayment()
        if pay_obj:
            # 2) Test the connection
            conn = one_line.networkIsAlive(URL=pay_obj.url, token=pay_obj.token)
            # print(conn)
            # active_id = self._context.get('active_id')# active id of the payment  with_context
            if conn:                     
                # 4) Get the data from wizard
                from_card = self.from_card_id.card_number
                to_card   = self.to_card_id.card_number
                ipn       = self.ipn
                amount    = self.sending_amount
                expDate  = self.format_data(self.expDate)
                
                # 5) Send the data as Json
                respond = one_line.cardToCardTransfer(
                    URL=pay_obj.url,
                    FROM_PAN=from_card,
                    toCard=to_card,
                    IPIN=ipn,
                    expDate=expDate,
                    tranAmount=amount,
                    dynamicFees=0,
                    token=pay_obj.token)
                # 6) Go and enjoy
                # print(respond)
                return respond
            return {'ok':False,'message': 'The network connection is not working, please check your connection and try again'}
     

    def format_data(self,date):
        year = str(date.year)
        month = str(date.month)
        
        if len(month) == 1:
            month = "0"+ month
        
        return year[2:]+month

