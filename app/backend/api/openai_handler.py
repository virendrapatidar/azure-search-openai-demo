import openai
from flask import session

class OpenaiHandler():

    def __init__(self,  gpt_deployment: str, chatgpt_deployment:str):
        self.gpt_deployment = gpt_deployment
        self.chatgpt_deployment = chatgpt_deployment

    # Define the function to get completion
    def get_completion(self, prompt):
        response = openai.Completion.create(
            engine=self.gpt_deployment,
            prompt=prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.7,
        )
        completion = response.choices[0].text.strip()
        return completion

    def extract_intent(self, text):
        response = openai.Completion.create(
            engine=self.gpt_deployment,
            prompt=f"""Extract the intent from the following text: '{text}'. 
            If user ask for Sasai products or services, use intent 'general'. 
            If user wants to send money, get quote, exchange rate, remittance fee etc then use intent 'action'. 
            Concise your answer to one word only. Intent:""",
            max_tokens=1,
            n=1,
            stop=["\n"],
            temperature=1,
        )
        intent = response.choices[0].text.strip()
        return intent.lower() 
    
    def get_chat_history_as_text(self, history, include_last_turn=True, approx_max_tokens=500) -> str:
        history_text = ""
        for h in reversed(history if include_last_turn else history[:-1]):
            history_text = """<|im_start|>user""" + "\n" + h["user"] + "\n" + """<|im_end|>""" + "\n" + """<|im_start|>assistant""" + "\n" + (
                h.get("bot") + """<|im_end|>""" if h.get("bot") else "") + "\n" + history_text
            if len(history_text) > approx_max_tokens*4:
                break
        return history_text
    
    def get_intent(self, history) -> str:  
        intent = ""
        if 'intent' in session:
            intent = session['intent']
        if intent == None or intent == "" or intent == "\"" or intent == "'" or intent.lower() == "general":
            for h in reversed(history):                        
                intent = self.extract_intent(h.get("user"))
                session['intent'] = intent    
                break            
        return intent.strip()

    def clear_intent(self) -> str:
            session['intent'] = ""
