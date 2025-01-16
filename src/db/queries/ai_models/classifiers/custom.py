import nltk
from nltk.corpus import stopwords
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

from db.queries.ai_models.classifiers.base import BaseClassifier


nltk.download("stopwords")
LANGUAGE = "portuguese"


class CustomClassifier(BaseClassifier):
    def initialize(self):
        df = pd.read_json(f"data/custom_training_data.json")
        df["text"] = df.apply(
            lambda x: f'{x["objeto"]}\n{x["descricao"]}\n{x["descricao_comp"]}',
            axis=1,
        )
        df["result"] = df["approved"].apply(lambda x: 1 if x else 0)

        self.vectorizer = TfidfVectorizer(stop_words=stopwords.words(LANGUAGE))

        x = self.vectorizer.fit_transform(df["text"])
        y = df["result"]

        self.model = LinearSVC()
        self.model.fit(x, y)

    def classify(self, object, description, complete_description) -> bool:
        text = f"{object}\n{description}"
        if complete_description:
            text += f"\n{complete_description}"
        x = self.vectorizer.transform([text])
        return bool(self.model.predict(x)[0])
