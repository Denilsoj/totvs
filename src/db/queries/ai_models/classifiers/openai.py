import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

from db.queries.ai_models.classifiers.base import BaseClassifier
from db.queries.ai_models.classifiers.helpers import (
    INITIAL_PROMPT_OPENAI,
    TEMPLATE_MESSAGE,
)


load_dotenv()


class ResponseFormat(BaseModel):
    approved: bool
    # details: str


class OpenAIClassifier(BaseClassifier):
    def initialize(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""), timeout=5)
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": INITIAL_PROMPT_OPENAI},
            ],
        )

        self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": """
                    Veja a seguir um exemplo de como você pode fazer a classificação de um objeto e sua descrição:

                    <exemplos>
                    1. descricao:  "AQUISIÇÃO DE MOBILIÁRIOS E EQUIPAMENTOS ELETRÔNICOS DESTINADOS A SUPRIR A DEMANDA DA CASA LAR E SECRETÁRIA DE ASSISTÊNCIA SOCIAL DO MUNICÍPIO DE CAFELÂNDIA. ATRAVÉS DE RECURSOS DA EMENDA PARLAMENTAR BANCADA DO PARANÁ N°202371170013, REQUERIDO ATRAVÉS DA PROGRAMAÇÃO SISTEMA DE GESTÃO DE TRANSFERÊNCIA VOLUNTARIAS- SIGTV" 
                    resultado: false justificativa: "apesar do texto conter a palavra, nao se encaixa com o contexto de serviços que a empresa TOTVS oferece"
                    </exemplos>
                    <exemplos>
                    2. descricao:  "Contratação de empresa especializada para fornecimento de licenças de uso de software de gestão de processos, com garantia de atualização e suporte técnico, para atender as necessidades da Secretaria Municipal de Administração e Finanças, conforme especificações e quantitativos constantes no Termo de Referência, Anexo I do Edital."
                    resultado: true justificativa: "a descricao se encaixa com o contexto de serviços que a empresa TOTVS oferece"
                    </exemplos>
                """,
                }
            ],
        )

        print("OpenAI initialized")
        print(response.choices[0].message.content)

    def classify(self, object, description, complete_description) -> bool:
        response = self.client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": TEMPLATE_MESSAGE.format(
                        object=object,
                        description=description,
                        complete_description=complete_description,
                    ),
                },
            ],
            response_format=ResponseFormat,
        )
        print(response.choices[0].message.content)

        result = response.choices[0].message.parsed

        if not result:
            print("Error parsing response")
            print()
            return False

        print("Resultado:", "Aprovado" if result.approved else "Reprovado")
        # print("Análise:\n", result.details)
        print()
        return result.approved
