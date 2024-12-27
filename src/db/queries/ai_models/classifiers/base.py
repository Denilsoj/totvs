from abc import ABC, abstractmethod


class BaseClassifier(ABC):
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def classify(self, object, description) -> bool:
        pass
