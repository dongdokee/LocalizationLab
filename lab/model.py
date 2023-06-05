import pickle
from typing import Generic, TypeVar

import numpy as np

T = TypeVar("T")


class LocalizationModel(Generic[T]):
    def __init__(self):
        # TODO
        pass

    def train(self, x, y: T, *args, **kwargs):
        # TODO
        pass

    def predict(self, x, *args, **kwargs) -> T:
        # TODO
        pass

    def save_model(self, model_path: str):
        with open(model_path, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load_model(model_path: str):
        with open(model_path, "rb") as f:
            return pickle.load(f)
