from unittest.mock import AsyncMock, MagicMock

import pytest

from src.providers.riot.riot_provider import RiotProvider
from src.repositories.riot.riot_repository import RiotRepository
from src.schemas.riot.accounts import AccountDto
from src.schemas.riot.match import MatchDto


@pytest.mark.asyncio
class TestRiotRepository:
    @pytest.fixture
    def mock_provider(self):
        return MagicMock(spec=RiotProvider)

    @pytest.fixture
    def repository(self, mock_provider):
        return RiotRepository(provider=mock_provider)

    async def test_get_account_by_riot_id(self, repository, mock_provider):
        # Arrange
        game_name = "Teemo"
        tag_line = "EUW"
        api_response = {
            "puuid": "12345",
            "gameName": "Teemo",
            "tagLine": "EUW"
        }
        mock_provider.get_account_by_riot_id = AsyncMock(return_value=api_response)

        # Act
        result = await repository.get_account_by_riot_id(game_name, tag_line)

        # Assert
        assert isinstance(result, AccountDto)
        assert result.puuid == "12345"
        assert result.game_name == "Teemo"
        mock_provider.get_account_by_riot_id.assert_called_once_with(game_name, tag_line)

    async def test_get_match_details(self, repository, mock_provider):
        # Arrange
        match_id = "EUW1_123456"
        api_response = {
            "metadata": {
                "dataVersion": "2",
                "matchId": "EUW1_123456",
                "participants": ["p1", "p2"]
            },
            "info": {
                "gameCreation": 123456789,
                "gameDuration": 1200,
                "gameId": 123456,
                "gameMode": "CLASSIC",
                "gameName": "Normal",
                "gameStartTimestamp": 123456790,
                "gameType": "MATCHED_GAME",
                "gameVersion": "12.1",
                "mapId": 11,
                "platformId": "EUW1",
                "queueId": 420,
                "tournamentCode": None,
                "participants": [],
                "teams": []
            }
        }
        mock_provider.get_match_details = AsyncMock(return_value=api_response)

        # Act
        result = await repository.get_match_details(match_id)

        # Assert
        assert isinstance(result, MatchDto)
        assert result.metadata.match_id == "EUW1_123456"
        assert result.info.game_id == 123456
        mock_provider.get_match_details.assert_called_once_with(match_id)
