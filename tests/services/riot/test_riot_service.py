from unittest.mock import AsyncMock, MagicMock

import pytest

from src.repositories.riot.riot_repository import RiotRepository
from src.schemas.riot.accounts import AccountDto
from src.schemas.riot.ml import RiotMlDatasetDto
from src.services.riot.riot_service import RiotService


@pytest.mark.asyncio
class TestRiotService:
    @pytest.fixture
    def mock_repository(self):
        return MagicMock(spec=RiotRepository)

    @pytest.fixture
    def service(self, mock_repository):
        return RiotService(repository=mock_repository)

    async def test_get_account_by_riot_id(self, service, mock_repository):
        # Arrange
        game_name = "Teemo"
        tag_line = "EUW"
        expected_account = AccountDto(puuid="123", game_name="Teemo", tag_line="EUW")

        mock_repository.get_account_by_riot_id = AsyncMock(return_value=expected_account)

        # Act
        result = await service.get_account_by_riot_id(game_name, tag_line)

        # Assert
        assert result == expected_account
        mock_repository.get_account_by_riot_id.assert_called_once_with(game_name, tag_line)

    async def test_get_match_ids_by_puuid(self, service, mock_repository):
        # Arrange
        puuid = "123"
        expected_ids = ["match1", "match2"]
        mock_repository.get_match_ids_by_puuid = AsyncMock(return_value=expected_ids)

        # Act
        result = await service.get_match_ids_by_puuid(puuid)

        # Assert
        assert result == expected_ids
        mock_repository.get_match_ids_by_puuid.assert_called_once_with(puuid, 20)

    async def test_build_ml_dataset_from_puuid(self, service, mock_repository):
        expected_dataset = RiotMlDatasetDto(feature_names=["kills"], rows=[])
        service.ml_service.build_dataset_from_puuid = AsyncMock(return_value=expected_dataset)

        result = await service.build_ml_dataset_from_puuid("123", count=10)

        assert result == expected_dataset
        service.ml_service.build_dataset_from_puuid.assert_called_once_with(puuid="123", count=10)

    async def test_build_framework_dataset_from_puuid(self, service):
        strategy = object()
        expected_training_data = {"x": [], "y": []}
        service.ml_service.build_framework_dataset_from_puuid = AsyncMock(return_value=expected_training_data)

        result = await service.build_framework_dataset_from_puuid("123", strategy=strategy, count=5)

        assert result == expected_training_data
        service.ml_service.build_framework_dataset_from_puuid.assert_called_once_with(
            puuid="123",
            strategy=strategy,
            count=5,
        )
