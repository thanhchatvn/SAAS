# -*- coding: utf-8 -*-
from odoo.http import route, request, Controller
import json
from datetime import datetime

# class Pos2(http.Controller):
#     @http.route('/pos2/pos2/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos2/pos2/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos2.listing', {
#             'root': '/pos2/pos2',
#             'objects': http.request.env['pos2.pos2'].search([]),
#         })

#     @http.route('/pos2/pos2/objects/<model("pos2.pos2"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos2.object', {
#             'object': obj
#         })

class Pos_card2card_payment(Controller):

    def is_valid_json(self,data):
        try:
            json.loads(data)
            return True
        except:
            return False

    @route('/pos_card2card_payment/get_partner', auth="user", methods=['GET'], csrf=True)
    def get_partner(self, **post):
        content_type = ('Content-Type', 'application/json')
        # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        # print(post)

        partner_id = post.get('id') 
        # print(partner_id)
        domain = [ ('id', '=', partner_id)]
        # domain = [ ('partner_id.id', '=', partner_id), ('default_card', '=', True)]

        # card_info_obj = request.env['card.information'].search(domain)
        card_info_obj = request.env['res.partner'].search(domain)
        # print(card_info_obj)
        # print(card_info_obj.bank_ids)
        # print(card_info_obj.bank_ids.default_card)
        # print(card_info_obj.bank_ids.filtered(lambda x: x.default_card == True) )
        # res_partner_bank_obj = card_info_obj.bank_ids.filtered(lambda x: x.default_card == True)
        # card_number = res_partner_bank_obj.card_information_id.card_number
        # print(card_number)
        # print(card_info_obj.bank_ids.card_information_id)
        # print(card_info_obj.bank_ids.filtered(lambda x: x.default_card == True) )
        # print(card_info_obj.bank_ids.card_information_id)
        # print(card_info_obj.bank_ids.card_information_id.card_number)
        
        # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        if card_info_obj:
            res_partner_bank_obj = card_info_obj.bank_ids.filtered(lambda x: x.default_card == True)
            card_number = res_partner_bank_obj.card_information_id.card_number
            exp_date  = res_partner_bank_obj.card_information_id.end_date
            str_exp_data = exp_date.strftime("%Y-%m-%d") 

            partner_card_info = {
                'card_number':card_number,
                'end_date': str_exp_data,
                'error': False
            }
            # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            partner_card_info_json = json.dumps(partner_card_info)
            return request.make_response(partner_card_info_json, headers=[ content_type ] )
        else:
            partner_card_info = {
                'message':"This client does not have a default card, please insert one.",
                'error': True
            }
            partner_card_info_json = json.dumps(partner_card_info)
            return request.make_response(partner_card_info_json, headers=[ content_type ] )
        # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

    @route('/pos_card2card_payment/get_journal_bank_card', auth="user", methods=['GET'], csrf=True)
    def get_journal_bank_card(self, **post):
        content_type = ('Content-Type', 'application/json')
        # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        # print(post)

        journal_ids = post.get('ids').split(',') 
        # journal_ids = post.get('ids') 
        # print(journal_ids)
        domain = [ ('id', 'in', journal_ids) ]

        journal_obj = request.env['account.journal'].search(domain)
        # card_info_obj = request.env['res.partner.bank'].search_read(domain=[])
        # print(res_bank_info_obj.bank_id.card_information_id)
        # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        #TODO: IF there is more than one journal fetch the related data and then send them
        journal_card_to_card_payment = {}
        journal_card_payment = {}
        if journal_obj:
            for journal in journal_obj: 
                journal_card_to_card_payment[journal.id] = journal.card_to_card_payment
                journal_card_payment[journal.id] = journal.bank_account_id.card_information_id.card_number
        # print(journal_card_to_card_payment)
        # print(journal_card_payment)
        # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            bank_card_info = {
                'is_used_in_pos':journal_card_to_card_payment,
                'card_number':journal_card_payment,
                'error': False
            }
            # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            bank_card_info_json = json.dumps(bank_card_info)
            return request.make_response(bank_card_info_json, headers=[ content_type ] )
        else:
            bank_card_info = {
                'message':"This journal dont have a card number, please fill it.",
                'error': True
            }
            bank_card_info_json = json.dumps(bank_card_info)
            return request.make_response(bank_card_info_json, headers=[ content_type ] )

        