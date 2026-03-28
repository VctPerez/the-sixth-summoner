import asyncio
from typing import Any

from src.repositories.riot.riot_repository import RiotRepository
from src.schemas.riot.ml import RiotMlDatasetDto
from src.services.riot.ml.riot_feature_parser import RiotFeatureParser
from src.services.riot.ml.strategies.base_strategy import FrameworkStrategy


class RiotMlService:
    def __init__(self, repository: RiotRepository, parser: RiotFeatureParser | None = None):
        self.repository = repository
        self.parser = parser or RiotFeatureParser()

    async def build_dataset_from_puuid(self, puuid: str, count: int = 20) -> RiotMlDatasetDto:
        match_ids = await self.repository.get_match_ids_by_puuid(puuid, count)
        if not match_ids:
            return RiotMlDatasetDto(feature_names=self.parser.feature_names, rows=[])

        tasks = [self.repository.get_match_details(match_id) for match_id in match_ids]
        matches = await asyncio.gather(*tasks)
        return self.parser.build_dataset(list(matches))

    async def build_framework_dataset_from_puuid(
            self,
            puuid: str,
            strategy: FrameworkStrategy,
            count: int = 20,
    ) -> Any:
        dataset = await self.build_dataset_from_puuid(puuid=puuid, count=count)
        return strategy.build_training_data(dataset)
