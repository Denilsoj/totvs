from src.db.queries.ai_models.classifiers.base import BaseClassifier
from src.db.queries.ai_models.classifiers.custom import CustomClassifier
from src.db.queries.ai_models.classifiers.gemini import GeminiClassifier
from src.db.queries.ai_models.classifiers.openai import OpenAIClassifier


class ContextClassifier:
    models: dict[str, type[BaseClassifier]] = {
        "gemini": GeminiClassifier,
        "openai": OpenAIClassifier,
        "custom": CustomClassifier,
    }

    def __init__(self, model: str):
        if model not in self.models:
            raise ValueError(f"Invalid model: {model}")

        self.model = self.models[model]()
        self.model.initialize()

    def execute(self, object, description, complete_description) -> bool:
        return self.model.classify(object, description, complete_description)
