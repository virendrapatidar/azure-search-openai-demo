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
        2. What is the receiving country? 
        If sending country United Kingdom then receiving country can be only Bangladesh, Botswana, Burundi, Cameroon, China, Ethiopia, Gambia, Ghana, India, Kenya, Malawi, Mozambique, Namibia, Nigeria, Pakistan, Philippines, Rwanda, Senegal, Somalia, South Africa, Tanzania, Uganda, Zambia or Zimbabwe. 
        If sending country South Africa then receiving country can be only Bangladesh, Botswana, Burundi, Cameroon, China, Congo, Ethiopia, Ghana, India, Kenya, Malawi, Nigeria, Pakistan, Rwanda, Senegal, Somalia, Tanzania, Uganda, Zambia or Zimbabwe.         
        If user enter any other receiving country, apologize and take user input again.
        3. How much money would you like to send? It should be positive number.
        
        If user do not provide any of above information, then ask followup questions to enter the missing inputs.
        
        Please provide your response in the following format
        "Sending country: <sending_country>, Receiving country: <receiving_country>, Amount: <amount>" 
        
        This API is also used to calculate fee, exchange rate to send money.
        """
        response = self.openai_handler.get_completion(quote_prompt)
        print("Bot:", response)
        jsonStr = self.parse_values(history)        
        isValid = self.validate_json(jsonStr)
        print ("isValid:" , isValid)
        result = quote_prompt
        if(isValid):
            response = self.prepare_request(jsonStr)
            self.openai_handler.clear_intent()
            # return self.format_response(response)
            result = str(response)
        response = {
            "prompt": quote_prompt,
            "result": result
        }
        return response

    def format_response(self, response):
        response_prompt = "Show JSON response in html table format. \n " + str(response)
        formatted_response = self.openai_handler.get_completion(response_prompt)
        return formatted_response


    def parse_values(self, history) -> str:
        text_history = self.openai_handler.get_chat_history_as_text(history)
        quote_prompt = """ Extract Sending country: sending_country, Receiving country: receiving_country, Amount: amount without currency code in json format. Do not return any other text with json        
        """
        jsonStr = self.openai_handler.get_completion(text_history + quote_prompt)
        jsonStr = re.sub("\n","",jsonStr)
        jsonStr = re.sub("<\|im_end\|>","",jsonStr)   
        print ("jsonStr: " + jsonStr)         
        return jsonStr
        
    def  validate_json(self, jsonStr):
        if(jsonStr.startswith("{")):
            try:
                jsonObj = json.loads(jsonStr)
                if((jsonObj["amount"] != "" and float(jsonObj["amount"]) > 0) 
                   and jsonObj["sending_country"] != "" and jsonObj["sending_country"] is not None 
                   and jsonObj["receiving_country"] != "" and jsonObj["receiving_country"] is not None):
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
        print("sending_country", jsonObj["sending_country"])
        print("receiving_country", jsonObj["receiving_country"])
        print("amount", jsonObj["amount"])

        if(jsonObj["sending_country"].lower() == "south africa" or jsonObj["sending_country"].lower() == "sa"):
            sending_country = 204
            sending_currency = 181
            if(jsonObj["receiving_country"].lower() == "bangladesh" or jsonObj["receiving_country"].lower() == "bd"):
                receiving_country = 19
                receiving_currency = 13
                product = 60            
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
            elif(jsonObj["receiving_country"].lower() == "india" or jsonObj["receiving_country"].lower() == "in"):
                receiving_country = 101
                receiving_currency = 68
                product = 21                             
            elif(jsonObj["receiving_country"].lower() == "kenya" or jsonObj["receiving_country"].lower() == "ke"):
                receiving_country = 114
                receiving_currency = 75
                product = 24
            elif(jsonObj["receiving_country"].lower() == "malawi" or jsonObj["receiving_country"].lower() == "mw"):
                receiving_country = 132
                receiving_currency = 103
                product = 48
            elif(jsonObj["receiving_country"].lower() == "nigeria" or jsonObj["receiving_country"].lower() == "ng"):
                receiving_country = 161
                receiving_currency = 153
                product = 46
            elif(jsonObj["receiving_country"].lower() == "pakistan" or jsonObj["receiving_country"].lower() == "pk"):
                receiving_country = 167
                receiving_currency = 119
                product = 27   
            elif(jsonObj["receiving_country"].lower() == "rawanda" or jsonObj["receiving_country"].lower() == "rw"):
                receiving_country = 183
                receiving_currency = 126
                product = 69
            elif(jsonObj["receiving_country"].lower() == "senegal" or jsonObj["receiving_country"].lower() == "sn"):
                receiving_country = 195
                receiving_currency = 174
                product = 234
            elif(jsonObj["receiving_country"].lower() == "somalia" or jsonObj["receiving_country"].lower() == "so"):
                receiving_country = 203
                receiving_currency = 153
                product = 41
            elif(jsonObj["receiving_country"].lower() == "tanzania" or jsonObj["receiving_country"].lower() == "tz"):
                receiving_country = 217
                receiving_currency = 150
                product = 68
            elif(jsonObj["receiving_country"].lower() == "uganda" or jsonObj["receiving_country"].lower() == "ug"):
                receiving_country = 229
                receiving_currency = 152
                product = 35
            elif(jsonObj["receiving_country"].lower() == "zambia" or jsonObj["receiving_country"].lower() == "zm"):
                receiving_country = 245
                receiving_currency = 182
                product = 237
            elif(jsonObj["receiving_country"].lower() == "zimbabwe" or jsonObj["receiving_country"].lower() == "zw"):
                receiving_country = 246
                receiving_currency = 75
                product = 24                                             

        elif(jsonObj["sending_country"].lower() == "united kingdom" or jsonObj["sending_country"].lower() == "uk"):
            sending_country = 232
            sending_currency = 53
            if(jsonObj["receiving_country"].lower() == "bangladesh" or jsonObj["receiving_country"].lower() == "bd"):
                receiving_country = 19
                receiving_currency = 13
                product = 22
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
            elif(jsonObj["receiving_country"].lower() == "gambia" or jsonObj["receiving_country"].lower() == "gm"):
                receiving_country = 79
                receiving_currency =  57
                product =  96
            elif(jsonObj["receiving_country"].lower() == "ghana" or jsonObj["receiving_country"].lower() == "gh"):
                receiving_country = 82
                receiving_currency = 55
                product = 77
            elif(jsonObj["receiving_country"].lower() == "india" or jsonObj["receiving_country"].lower() == "in"):
                receiving_country = 101
                receiving_currency = 68
                product = 29                             
            elif(jsonObj["receiving_country"].lower() == "kenya" or jsonObj["receiving_country"].lower() == "ke"):
                receiving_country = 114
                receiving_currency = 75
                product = 24
            elif(jsonObj["receiving_country"].lower() == "malawi" or jsonObj["receiving_country"].lower() == "mw"):
                receiving_country = 150
                receiving_currency =  103
                product =  76
            elif(jsonObj["receiving_country"].lower() == "mozambique" or jsonObj["receiving_country"].lower() == "mz"):
                receiving_country = 79
                receiving_currency = 107
                product =  39
            elif(jsonObj["receiving_country"].lower() == "namibia" or jsonObj["receiving_country"].lower() == "na"):
                receiving_country = 152
                receiving_currency =  108
                product =  6
            elif(jsonObj["receiving_country"].lower() == "nigeria" or jsonObj["receiving_country"].lower() == "ng"):
                receiving_country = 161
                receiving_currency =  153
                product =  74
            elif(jsonObj["receiving_country"].lower() == "pakistan" or jsonObj["receiving_country"].lower() == "pk"):
                receiving_country = 167
                receiving_currency = 119
                product = 34
            elif(jsonObj["receiving_country"].lower() == "philippines" or jsonObj["receiving_country"].lower() == "ph"):
                receiving_country = 174
                receiving_currency =  118
                product =  59
            elif(jsonObj["receiving_country"].lower() == "rawanda" or jsonObj["receiving_country"].lower() == "rw"):
                receiving_country = 183
                receiving_currency = 126
                product = 40
            elif(jsonObj["receiving_country"].lower() == "senegal" or jsonObj["receiving_country"].lower() == "sn"):
                receiving_country = 195
                receiving_currency = 174
                product = 45
            elif(jsonObj["receiving_country"].lower() == "somalia" or jsonObj["receiving_country"].lower() == "so"):
                receiving_country = 203
                receiving_currency = 153
                product = 69
            elif(jsonObj["receiving_country"].lower() == "south africa" or jsonObj["receiving_country"].lower() == "sa"):
                receiving_country = 204
                receiving_currency = 181
                product = 5
            elif(jsonObj["receiving_country"].lower() == "tanzania" or jsonObj["receiving_country"].lower() == "tz"):
                receiving_country = 217
                receiving_currency = 150
                product = 79
            elif(jsonObj["receiving_country"].lower() == "uganda" or jsonObj["receiving_country"].lower() == "ug"):
                receiving_country = 229
                receiving_currency = 152
                product = 65
            elif(jsonObj["receiving_country"].lower() == "zambia" or jsonObj["receiving_country"].lower() == "zm"):
                receiving_country = 245
                receiving_currency = 182
                product = 43
            elif(jsonObj["receiving_country"].lower() == "zimbabwe" or jsonObj["receiving_country"].lower() == "zw"):
                receiving_country = 246
                receiving_currency = 153
                product = 15
         
        endpoint = "calculate/"
        amount = jsonObj["amount"]

        print("sending_country_code", sending_country)
        print("sending_currency_code", sending_currency)
        print("receiving_country_code", receiving_country)
        print("receiving_currency_code", receiving_currency)
        print("product_code", product)
        print("amount", amount)

        req_data = self.prepare_quotes_request_json(amount, receiving_country, receiving_currency, product, sending_country, sending_currency)
        isUk = sending_country == 232
        response = self.request_handler.post_request(endpoint, req_data, isUk)
        print(response)
        if(response is not None and response.get("data") is not None):
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
        return ""

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

