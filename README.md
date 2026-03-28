# the-sixth-summoner

## ML dataset pipeline

The project now includes a small ML preparation layer that turns Riot match data
into tabular features and exposes a strategy-based output for different
frameworks.

### Main pieces

- `src/services/riot/ml/riot_feature_parser.py`: parses `MatchDto` into feature rows.
- `src/schemas/riot/ml/dataset_dto.py`: pydantic DTOs for feature rows and datasets.
- `src/services/riot/ml/strategies/sklearn_strategy.py`: returns pandas DataFrame/Series.
- `src/services/riot/ml/strategies/torch_strategy.py`: returns PyTorch tensors.
- `src/services/riot/ml/riot_ml_service.py`: orchestrates repository fetch + parse + strategy.

### Example usage

```python
from src.providers.riot.riot_provider import RiotProvider
from src.repositories.riot.riot_repository import RiotRepository
from src.services.riot.riot_service import RiotService
from src.services.riot.ml.strategies import SklearnStrategy, TorchStrategy

provider = RiotProvider(api_key="<riot-api-key>")
repository = RiotRepository(provider=provider)
service = RiotService(repository=repository)

# Base dataset DTO
dataset = await service.build_ml_dataset_from_puuid("<puuid>", count=20)

# Framework-specific payloads
sklearn_data = await service.build_framework_dataset_from_puuid(
    puuid="<puuid>",
    strategy=SklearnStrategy(),
    count=20,
)

torch_data = await service.build_framework_dataset_from_puuid(
    puuid="<puuid>",
    strategy=TorchStrategy(),
    count=20,
)
```

Install optional dependencies depending on your framework choice:

- `ml-sklearn` for scikit-learn workflows
- `ml-torch` for PyTorch workflows
