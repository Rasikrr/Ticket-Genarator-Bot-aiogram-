import openai
import os
from dotenv import load_dotenv

load_dotenv()


class ChatGPT:
    def __init__(self):
        self.model_id = "gpt-3.5-turbo"
        openai.api_key = os.getenv("OPENAI")

    def ask_to_ai(self, message):
        response = openai.ChatCompletion.create(
            model=self.model_id,
            messages=[{"role": "user", "content": f"{message}"}]
        )
        return response["choices"][0]["message"]["content"]


