import requests

from approaches.approach import Approach
from api.openai_handler import OpenaiHandler
from api.request_handler import RequestHandler
import json
import re


class Quotes(Approach):
    sending_country = ""
    receiving_country = ""
    amount = ""
    def __init__(self,  gpt_deployment: str, chatgpt_deployment: str):
        self.gpt_deployment = gpt_deployment
        self.chatgpt_deployment = chatgpt_deployment
        self.openai_handler =  OpenaiHandler(gpt_deployment, chatgpt_deployment)
        self.request_handler = RequestHandler()
        
   
    # Define the function to handle the conversation with the user
    def run(self, history: str, overrides: dict) -> any:
        quote_prompt = """ Ask below questions for quotes. All questions should get answer from user.
        
        1. What is the sending country? It can be only South Africa or United Kingdom. If user enter any other country, apologize and take user input again.
        2. What is the receiving country? It can be only India, Kenya, Bangladesh, Zimbabwe, Botswana, China, Ethiopia, Pakistan or Ghana. If user enter any other country, apologize and take user input again.
        3. How much money would you like to send? It should be positive number.
        
        If user do not provide any of above information, then ask followup questions to enter the missing inputs.
        
        Please provide your response in the following format
        "Sending country: <sending_country>, Receiving country: <receiving_country>, Amount: <amount>" 
        """
        response = self.openai_handler.get_completion(quote_prompt)
        print("Bot:", response)
        jsonStr = self.parse_values(history)        
        isValid = self.validate_json(jsonStr)
        print ("isValid:" , isValid)
        if(isValid):
            response = self.prepare_request(jsonStr)
            self.openai_handler.clear_intent()
            # return self.format_response(response)
            return str(response)
        return quote_prompt

    def format_response(self, response):
        response_prompt = "Show JSON response in html table format. \n " + str(response)
        formatted_response = self.openai_handler.get_completion(response_prompt)
        return formatted_response


    def parse_values(self, history) -> str:
        text_history = self.openai_handler.get_chat_history_as_text(history)
        quote_prompt = """ Extract Sending country: sending_country, Receiving country: receiving_country, Amount: amount without currency code in json format. Do not return any other text with json        
        """
        jsonStr = self.openai_handler.get_completion(text_history + quote_prompt)
        if(jsonStr.startswith("{")):
            jsonStr = re.sub("\n","",jsonStr)
            jsonStr = re.sub("<\|im_end\|>","",jsonStr)        
        return jsonStr
        
    def  validate_json(self, jsonStr):
        if(jsonStr.startswith("{")):
            try:
                jsonObj = json.loads(jsonStr)
                if((jsonObj["amount"] != "" and float(jsonObj["amount"]) > 0) and jsonObj["sending_country"] != "" and jsonObj["receiving_country"] != ""):
                    return True
            except:
                print("not valid json" + jsonStr)
        return False
    
    def prepare_request(self, jsonStr):
        jsonObj = json.loads(jsonStr)
        sending_country = 0  
        sending_currency = 0
        receiving_country = 0
        receiving_currency = 0
        product = 0

        if(jsonObj["sending_country"].lower() == "South Africa" or jsonObj["sending_country"].lower() == "sa"):
            if(jsonObj["receiving_country"].lower() == "india" or jsonObj["receiving_country"].lower() == "in"):
                receiving_country = 101
                receiving_currency = 68
                product = 21                             
            elif(jsonObj["receiving_country"].lower() == "bangladesh" or jsonObj["receiving_country"].lower() == "bd"):
                receiving_country = 19
                receiving_currency = 13
                product = 60
            elif(jsonObj["receiving_country"].lower() == "zimbabwe" or jsonObj["receiving_country"].lower() == "zw"):
                receiving_country = 246
                receiving_currency = 75
                product = 24
            elif(jsonObj["receiving_country"].lower() == "botswana" or jsonObj["receiving_country"].lower() == "bw"):
                receiving_country = 29
                receiving_currency = 24
                product = 56
            elif(jsonObj["receiving_country"].lower() == "burundi" or jsonObj["receiving_country"].lower() == "bi"):
                receiving_country = 29
                receiving_currency = 16
                product = 231
            elif(jsonObj["receiving_country"].lower() == "cameroon" or jsonObj["receiving_country"].lower() == "cm"):
                receiving_country = 38
                receiving_currency = 163
                product = 57
            elif(jsonObj["receiving_country"].lower() == "china" or jsonObj["receiving_country"].lower() == "cn"):
                receiving_country = 86
                receiving_currency = 34
                product = 39
            elif(jsonObj["receiving_country"].lower() == "congo" or jsonObj["receiving_country"].lower() == "cd"):
                receiving_country = 51
                receiving_currency = 153
                product = 74
            elif(jsonObj["receiving_country"].lower() == "ethiopia" or jsonObj["receiving_country"].lower() == "et"):
                receiving_country = 251
                receiving_currency = 49
                product = 32
            elif(jsonObj["receiving_country"].lower() == "ghana" or jsonObj["receiving_country"].lower() == "gh"):
                receiving_country = 82
                receiving_currency = 55
                product = 49
            elif(jsonObj["receiving_country"].lower() == "kenya" or jsonObj["receiving_country"].lower() == "ke"):
                receiving_country = 114
                receiving_currency = 75
                product = 24
            elif(jsonObj["receiving_country"].lower() == "pakistan" or jsonObj["receiving_country"].lower() == "pk"):
                receiving_country = 167
                receiving_currency = 119
                product = 27
                                  

        elif(jsonObj["sending_country"].lower() == "United Kingdom" or jsonObj["sending_country"].lower() == "uk"):
            sending_country = 232
            sending_currency = 53
            if(jsonObj["receiving_country"].lower() == "india" or jsonObj["receiving_country"].lower() == "in"):
                receiving_country = 101
                receiving_currency = 68
                product = 29                             
            elif(jsonObj["receiving_country"].lower() == "bangladesh" or jsonObj["receiving_country"].lower() == "bd"):
                receiving_country = 19
                receiving_currency = 13
                product = 22
            elif(jsonObj["receiving_country"].lower() == "zimbabwe" or jsonObj["receiving_country"].lower() == "zw"):
                receiving_country = 19
                receiving_currency = 153
                product = 15
            elif(jsonObj["receiving_country"].lower() == "botswana" or jsonObj["receiving_country"].lower() == "bw"):
                receiving_country = 29
                receiving_currency = 24
                product = 85
            elif(jsonObj["receiving_country"].lower() == "burundi" or jsonObj["receiving_country"].lower() == "bi"):
                receiving_country = 29
                receiving_currency = 16
                product = 97
            elif(jsonObj["receiving_country"].lower() == "cameroon" or jsonObj["receiving_country"].lower() == "cm"):
                receiving_country = 38
                receiving_currency = 163
                product = 86
            elif(jsonObj["receiving_country"].lower() == "china" or jsonObj["receiving_country"].lower() == "cn"):
                receiving_country = 86
                receiving_currency = 34
                product = 67
            elif(jsonObj["receiving_country"].lower() == "ethiopia" or jsonObj["receiving_country"].lower() == "et"):
                receiving_country = 251
                receiving_currency = 49
                product = 62
            elif(jsonObj["receiving_country"].lower() == "ghana" or jsonObj["receiving_country"].lower() == "gh"):
                receiving_country = 82
                receiving_currency = 55
                product = 77
            elif(jsonObj["receiving_country"].lower() == "kenya" or jsonObj["receiving_country"].lower() == "ke"):
                receiving_country = 114
                receiving_currency = 75
                product = 24
            elif(jsonObj["receiving_country"].lower() == "pakistan" or jsonObj["receiving_country"].lower() == "pk"):
                receiving_country = 167
                receiving_currency = 119
                product = 34
   

        endpoint = "calculate/"
        amount = jsonObj["amount"]

        print("sending_country", sending_country)
        print("sending_currency", sending_currency)
        print("receiving_country", receiving_country)
        print("receiving_currency", receiving_currency)
        print("product", product)
        print("amount", amount)

        req_data = self.prepare_quotes_request_json(amount, receiving_country, receiving_currency, product, sending_country, sending_currency)
        isUk = sending_country == 232
        response = self.request_handler.post_request(endpoint, req_data, isUk)
        print(response)
        responseAttr = response.get("data").get("attributes")
        required_json = {
            "sending_amount" : responseAttr.get("sending_amount"),            
            "recipient_amount" : responseAttr.get("recipient_amount"),
            "exchange_rate" : responseAttr.get("rate"),
            "total_amount_to_pay" : float(responseAttr.get("amount_to_pay")) + float(responseAttr.get("vat")),
            "fees" : responseAttr.get("fees"),
            "vat" : responseAttr.get("vat")
        }
        return required_json

    def prepare_quotes_request_json(self, amount, receiving_country, receiving_currency, product, sending_country, sending_currency):
        quote_req_json = {
            "data": {
                "type": "calculation_requests",
                "id": "null",
                "attributes": {
                "receive": False,
                "amount": amount
                },
                "relationships": {
                "receiving_country": {
                    "data": {
                    "type": "countries",
                    "id": receiving_country
                    }
                },
                "sending_country": {
                    "data": {
                    "type": "countries",
                    "id": sending_country
                    }
                },
                "sending_currency": {
                    "data": {
                    "type": "currencies",
                    "id": sending_currency
                    }
                },
                "receiving_currency": {
                    "data": {
                    "type": "currencies",
                    "id": receiving_currency
                    }
                },
                "product": {
                    "data": {
                    "type": "products",
                    "id": product
                    }
                }
                }
            }
        }
        return quote_req_json

