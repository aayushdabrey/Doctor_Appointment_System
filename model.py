from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

import os
load_dotenv()
api_key = os.environ["OPENAI_API_KEY"]

class Model:
    def __init__(self) ->None:
        self.model_name = 'gpt-4'
        self.api_key = api_key
    def get(self):
        model = ChatOpenAI(api_key=self.api_key,model=self.model_name)
        return model
        