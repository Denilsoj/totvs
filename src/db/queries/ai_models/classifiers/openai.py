import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

from db.queries.ai_models.classifiers.base import BaseClassifier
from db.queries.ai_models.classifiers.helpers import INITIAL_PROMPT, TEMPLATE_MESSAGE


load_dotenv()


class ResponseFormat(BaseModel):
    approved: bool
    # details: str


class OpenAIClassifier(BaseClassifier):
    def initialize(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""), timeout=5)
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": INITIAL_PROMPT},
            ],
        )
        print("OpenAI initialized")
        print(response.choices[0].message.content)

    def classify(self, object, description) -> bool:
        response = self.client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": TEMPLATE_MESSAGE.format(
                        object=object, description=description
                    ),
                },
            ],
            response_format=ResponseFormat,
        )

        result = response.choices[0].message.parsed

        if not result:
            print("Error parsing response")
            print()
            return False

        print("Resultado:", "Aprovado" if result.approved else "Reprovado")
        # print("Análise:\n", result.details)
        print()
        return result.approved
