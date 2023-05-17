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
            engine=self.chatgpt_deployment,
            prompt=f"Extract the intent from the following text: '{text}'. you can classify intent in 2 category. first is “general” and other is quote . We use general intent for document search and quote intent to get remittance quotations. Answer everything general if user input is not having a context of a user. Concise your answer to one word only. \nIntent:",
            max_tokens=1,
            n=1,
            stop=["\n"],
            temperature=0.5,
        )
        intent = response.choices[0].text.strip()
        return intent    
    
    def get_chat_history_as_text(self, history, include_last_turn=True, approx_max_tokens=500) -> str:
        history_text = ""
        for h in reversed(history if include_last_turn else history[:-1]):
            history_text = """<|im_start|>user""" + "\n" + h["user"] + "\n" + """<|im_end|>""" + "\n" + """<|im_start|>assistant""" + "\n" + (
                h.get("bot") + """<|im_end|>""" if h.get("bot") else "") + "\n" + history_text
            if len(history_text) > approx_max_tokens*4:
                break
        return history_text
    
    def get_intent(self, history) -> str:  
        intent = None
        if 'intent' in session:
            intent = session['intent']
        if intent == None or intent == "" :
            for h in reversed(history):                        
                intent = self.extract_intent(h)
                session['intent'] = intent
                break
        return intent

    def clear_intent(self) -> str:
            session['intent'] = None
