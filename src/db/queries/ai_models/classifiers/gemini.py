import os

import google.generativeai as genai
from dotenv import load_dotenv

from db.queries.ai_models.classifiers.base import BaseClassifier
from db.queries.ai_models.classifiers.helpers import INITIAL_PROMPT, TEMPLATE_MESSAGE


load_dotenv()

genai.configure(api_key=os.environ.get("GOOGLE_GENERATIVEAI_API_KEY", ""))


class GeminiClassifier(BaseClassifier):
    def __init__(self) -> None:
        gemini = genai.GenerativeModel("gemini-1.5-flash")
        self.chat = gemini.start_chat()

    def initialize(self):
        self.chat.send_message(INITIAL_PROMPT)

    def classify(self, object: str, description: str) -> bool:
        result = self.chat.send_message(
            TEMPLATE_MESSAGE.format(object=object, description=description)
        )

        return True if str.strip(result.text) == "sim" else False
