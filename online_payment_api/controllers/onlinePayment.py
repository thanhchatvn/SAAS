import json
import os

import requests
import subprocess as notify_message


class oneLinePayment:

    def __init__(self):
        pass

    def authentication(self, URL=None, username=None, password=None, rememberMe=False):

        try:
            res = requests.post(
                URL + "authenticate",
                headers={'Content-Type': 'application/json'},
                json={'username': username, 'password': password, 'rememberMe': rememberMe}
            )

            # Get the authorization object

            token = res.headers["Authorization"]

            return token
        except:
            
            notify_message.call(['notify-send','Connection','The connection is not stable, check you network connection and try again'])
            

    def networkIsAlive(self, URL=None, token=None):

        try:

            res = requests.get(
                URL + "v1/isAlive",
                headers={'Content-Type': 'application/json', 'Authorization': token},

            )

            if res.status_code == 200:
                return True
            return False
        except:
            notify_message.call(['notify-send','Connection','The connection is not stable, check you network connection and try again'])
            return False
            
    def cardToCardTransfer(self, URL=None, FROM_PAN=None, toCard=None, IPIN=None, expDate=None, tranAmount=None,
                           dynamicFees=0, token=None):
        req_url = URL + "v1/doCardTransfer"
        req_header = {'Content-Type': 'application/json', 'Authorization': token}
        # print(req_url)
        req_json = {
            "PAN": FROM_PAN,
            "toCard": toCard,
            "IPIN": IPIN,
            "expDate": expDate,
            "tranAmount": tranAmount,
            "dynamicFees": dynamicFees
        }

        try:
            res = requests.post(
                req_url,
                headers=req_header,
                json=req_json
            )

            res_text = res.text
            res_json = json.loads(res_text)
            # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            # print(res_json)

            if res.status_code == 200:
            # if res_json["responseStatus"] == 0:
                
                # success_message = f'From card : {FROM_PAN} To card   : {toCard} The amount: {amount}'
                
                # notify_message.call(['notify-send','Transformation','The transformation was successful'])
                return { "ok":True,"message": res_json["responseMessage"]}
            
            # notify_message.call(['notify-send','Transformation',res_json["responseMessage"]])
            # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            return { "ok":False,"message": res_json["responseMessage"]}
        except:
            notify_message.call(['notify-send','Transformation','The card to card transformation is failed, du to connectipon'])
            return { "ok":False,"message":'The card to card transformation is failed, du to connectipon' }
            


# if __name__ == "__main__":
#     pay = oneLinePayment()
#     # pay.networkIsAlive()
