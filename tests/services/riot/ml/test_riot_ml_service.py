from unittest.mock import AsyncMock, MagicMock

import pytest

from src.repositories.riot.riot_repository import RiotRepository
from src.schemas.riot.ml import MatchFeatureRowDto, RiotMlDatasetDto
from src.services.riot.ml.riot_feature_parser import RiotFeatureParser
from src.services.riot.ml.riot_ml_service import RiotMlService


class _DummyStrategy:
    def build_training_data(self, dataset: RiotMlDatasetDto) -> dict[str, object]:
        return {"rows": len(dataset.rows), "feature_names": dataset.feature_names}


@pytest.mark.asyncio
class TestRiotMlService:
    @pytest.fixture
    def mock_repository(self) -> MagicMock:
        return MagicMock(spec=RiotRepository)

    async def test_build_dataset_from_puuid_returns_empty_dataset_when_no_matches(self, mock_repository: MagicMock):
        mock_repository.get_match_ids_by_puuid = AsyncMock(return_value=[])
        service = RiotMlService(repository=mock_repository)

        dataset = await service.build_dataset_from_puuid("puuid-1", count=5)

        assert dataset.rows == []
        assert dataset.feature_names == RiotFeatureParser.feature_names
        mock_repository.get_match_ids_by_puuid.assert_called_once_with("puuid-1", 5)

    async def test_build_dataset_from_puuid_fetches_matches_and_parses(self, mock_repository: MagicMock):
        parser = MagicMock(spec=RiotFeatureParser)
        expected_dataset = RiotMlDatasetDto(
            feature_names=["kills"],
            rows=[
                MatchFeatureRowDto(
                    match_id="EUW1_1",
                    puuid="p1",
                    participant_id=1,
                    champion_id=266,
                    team_id=100,
                    queue_id=420,
                    game_duration_seconds=1800,
                    kills=3,
                    deaths=2,
                    assists=4,
                    kda_ratio=3.5,
                    gold_earned=10000,
                    total_damage_dealt_to_champions=15000,
                    vision_score=20,
                    total_cs=170,
                    team_kill_share=0.4,
                    prior_matches=0,
                    prior_win_rate=0.0,
                    win=True,
                )
            ],
        )

        parser.build_dataset.return_value = expected_dataset
        mock_repository.get_match_ids_by_puuid = AsyncMock(return_value=["EUW1_1", "EUW1_2"])
        mock_repository.get_match_details = AsyncMock(side_effect=[{"id": 1}, {"id": 2}])

        service = RiotMlService(repository=mock_repository, parser=parser)

        dataset = await service.build_dataset_from_puuid("puuid-1")

        assert dataset == expected_dataset
        parser.build_dataset.assert_called_once()
        parsed_matches = parser.build_dataset.call_args.args[0]
        assert parsed_matches == [{"id": 1}, {"id": 2}]

    async def test_build_framework_dataset_from_puuid_uses_strategy(self, mock_repository: MagicMock):
        parser = MagicMock(spec=RiotFeatureParser)
        parser_dataset = RiotMlDatasetDto(feature_names=["kills"], rows=[])
        parser.build_dataset.return_value = parser_dataset

        mock_repository.get_match_ids_by_puuid = AsyncMock(return_value=["EUW1_1"])
        mock_repository.get_match_details = AsyncMock(return_value={"id": 1})

        service = RiotMlService(repository=mock_repository, parser=parser)
        strategy = _DummyStrategy()

        training_data = await service.build_framework_dataset_from_puuid("puuid-1", strategy)

        assert training_data == {"rows": 0, "feature_names": ["kills"]}
