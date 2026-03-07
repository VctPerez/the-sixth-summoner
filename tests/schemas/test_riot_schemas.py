from src.schemas.riot.accounts.account_dto import AccountDto
from src.schemas.riot.match.match_dto import MatchDto


class TestRiotSchemas:
    def test_account_dto_aliasing(self):
        """Test that camelCase JSON is correctly parsed into snake_case fields for AccountDto."""
        json_data = {
            "puuid": "1234-5678",
            "gameName": "Teemo",
            "tagLine": "EUW"
        }

        account = AccountDto(**json_data)

        assert account.puuid == "1234-5678"
        assert account.game_name == "Teemo"
        assert account.tag_line == "EUW"

    def test_account_dto_serialization(self):
        """Test that AccountDto serializes back to camelCase."""
        account = AccountDto(puuid="1234-5678", game_name="Teemo", tag_line="EUW")

        dumped_data = account.model_dump(by_alias=True)

        assert dumped_data["gameName"] == "Teemo"
        assert dumped_data["tagLine"] == "EUW"
        assert "game_name" not in dumped_data

    def test_nested_match_dto_aliasing(self):
        """Test nested structure parsing with aliasing (list of strings and snake_case fields)."""
        json_data = {
            "metadata": {
                "dataVersion": "2",
                "matchId": "EUW1_123456",
                "participants": ["puuid1", "puuid2"]
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
                "participants": [],  # Empty list IS valid for list[ParticipantDto]
                "teams": []  # Empty list IS valid for list[TeamDto]
            }
        }

        match = MatchDto(**json_data)

        # Check conversion to snake_case
        assert match.metadata.data_version == "2"
        assert match.metadata.match_id == "EUW1_123456"
        assert match.info.game_creation == 123456789
        assert match.info.platform_id == "EUW1"
