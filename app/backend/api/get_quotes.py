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
        quote_prompt = """ Ask below questions for quotes. All questions should get answer.
        1. What is the sending country? It can be only South Africa or United Kingdom.
        2. What is the receiving country?
        3. How much money would you like to send?        
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
            return response
         
        return quote_prompt


    def parse_values(self, history) -> str:
        text_history = self.openai_handler.get_chat_history_as_text(history)
        quote_prompt = """ Extract Sending country: sending_country, Receiving country: receiving_country, Amount: amount without currency code in json format. Do not return any other text with json        
        """
        jsonStr = self.openai_handler.get_completion(text_history + quote_prompt)
        if(jsonStr.startswith("{")):
            jsonStr = re.sub("\n","",jsonStr)
            jsonStr = re.sub("<\|im_end\|>","",jsonStr)
        
        print("jsonStr:", jsonStr)            
        return jsonStr
        
    def  validate_json(self, jsonStr):
        if(jsonStr.startswith("{")):
            jsonObj = json.loads(jsonStr)
            if((jsonObj["amount"] != "" and float(jsonObj["amount"]) > 0) and jsonObj["sending_country"] != "" and jsonObj["receiving_country"] != ""):
                return True
        return False
    
    def prepare_request(self, jsonStr):
        jsonObj = json.loads(jsonStr)
        receiving_country = 101  # default india
        receiving_currency = 68 # default india
        product = 21 # default india

        if(jsonObj["receiving_country"].lower() == "india" or jsonObj["receiving_country"].lower() == "in"):
            receiving_country = 101
            receiving_currency = 68
        
        elif(jsonObj["receiving_country"].lower() == "bangladesh" or jsonObj["receiving_country"].lower() == "bd"):
            receiving_country = 19
            receiving_currency = 13
            product = 60

        sending_country = 204  # default SA
        sending_currency = 181 # default SA

        endpoint = "calculate/"
        amount = jsonObj["amount"]
        req_data = self.prepare_quotes_request_json(amount, receiving_country, receiving_currency, product, sending_country, sending_currency)
        response = self.request_handler.post_request(endpoint, req_data)
        print("Response", response)
        return response 

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

