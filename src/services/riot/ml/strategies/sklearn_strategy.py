import pandas as pd

from src.schemas.riot.ml import RiotMlDatasetDto
from src.services.riot.ml.strategies.base_strategy import FrameworkStrategy


class SklearnStrategy(FrameworkStrategy):
    def build_training_data(self, dataset: RiotMlDatasetDto) -> dict[str, object]:
        x_data, y_data = dataset.to_xy()

        x_frame = pd.DataFrame(x_data, columns=dataset.feature_names)
        y_series = pd.Series(y_data, name=dataset.target_name)

        return {
            "x": x_frame,
            "y": y_series,
            "feature_names": dataset.feature_names,
            "target_name": dataset.target_name,
        }
