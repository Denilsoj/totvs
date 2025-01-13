from db.queries.ai_models.classifiers.base import BaseClassifier
from db.queries.ai_models.classifiers.gemini import GeminiClassifier
from db.queries.ai_models.classifiers.openai import OpenAIClassifier


class ContextClassifier:
    models: dict[str, type[BaseClassifier]] = {
        "gemini": GeminiClassifier,
        "openai": OpenAIClassifier,
    }

    def __init__(self, model: str):
        if model not in self.models:
            raise ValueError(f"Invalid model: {model}")

        self.model = self.models[model]()
        self.model.initialize()

    def execute(self, object, description, complete_description) -> bool:
        return self.model.classify(object, description, complete_description)
