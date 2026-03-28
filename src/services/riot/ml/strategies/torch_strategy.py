import importlib

from src.schemas.riot.ml import RiotMlDatasetDto
from src.services.riot.ml.strategies.base_strategy import FrameworkStrategy


class TorchStrategy(FrameworkStrategy):
    def build_training_data(self, dataset: RiotMlDatasetDto) -> dict[str, object]:
        try:
            torch = importlib.import_module("torch")
        except ModuleNotFoundError as error:
            raise ImportError(
                "PyTorch is not installed. Install it to use TorchStrategy."
            ) from error

        x_data, y_data = dataset.to_xy()

        x_tensor = torch.tensor(x_data, dtype=torch.float32)
        y_tensor = torch.tensor(y_data, dtype=torch.float32)

        return {
            "x": x_tensor,
            "y": y_tensor,
            "feature_names": dataset.feature_names,
            "target_name": dataset.target_name,
        }
