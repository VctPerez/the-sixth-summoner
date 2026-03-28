from abc import ABC, abstractmethod
from typing import Any

from src.schemas.riot.ml import RiotMlDatasetDto


class FrameworkStrategy(ABC):
    @abstractmethod
    def build_training_data(self, dataset: RiotMlDatasetDto) -> Any:
        raise NotImplementedError
