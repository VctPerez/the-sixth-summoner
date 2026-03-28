from src.schemas.riot.accounts.account_dto import AccountDto
from src.schemas.riot.match.match_dto import MatchDto
from src.schemas.riot.ml import MatchFeatureRowDto, RiotMlDatasetDto
from src.schemas.riot.status import PlatformDataDto


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
        assert match.timeline is None

    def test_ml_row_aliasing_and_dataset_to_xy(self):
        json_data = {
            "matchId": "EUW1_42",
            "puuid": "abc",
            "participantId": 1,
            "championId": 157,
            "teamId": 100,
            "queueId": 420,
            "gameDurationSeconds": 1800,
            "kills": 10,
            "deaths": 2,
            "assists": 4,
            "kdaRatio": 7.0,
            "goldEarned": 12000,
            "totalDamageDealtToChampions": 25000,
            "visionScore": 30,
            "totalCs": 190,
            "teamKillShare": 0.5,
            "priorMatches": 5,
            "priorWinRate": 0.6,
            "win": True,
        }

        row = MatchFeatureRowDto(**json_data)
        dataset = RiotMlDatasetDto(feature_names=["kills", "assists", "kda_ratio"], rows=[row])
        x_data, y_data = dataset.to_xy()

        dumped = row.model_dump(by_alias=True)
        assert dumped["matchId"] == "EUW1_42"
        assert dumped["teamKillShare"] == 0.5
        assert x_data == [[10.0, 4.0, 7.0]]
        assert y_data == [1]

    def test_platform_status_aliasing(self):
        json_data = {
            "id": "EUW1",
            "name": "EU West",
            "locales": ["en_GB"],
            "maintenances": [],
            "incidents": [
                {
                    "id": 1,
                    "maintenanceStatus": "scheduled",
                    "incidentSeverity": "info",
                    "titles": [{"locale": "en_GB", "content": "Test"}],
                    "updates": [
                        {
                            "id": 10,
                            "author": "riot",
                            "publish": True,
                            "publishLocations": ["riotclient"],
                            "translations": [{"locale": "en_GB", "content": "Details"}],
                            "createdAt": "2026-01-01T00:00:00Z",
                            "updatedAt": "2026-01-01T00:01:00Z",
                        }
                    ],
                    "createdAt": "2026-01-01T00:00:00Z",
                    "archiveAt": None,
                    "updatedAt": "2026-01-01T00:05:00Z",
                    "platforms": ["windows"],
                }
            ],
        }

        dto = PlatformDataDto(**json_data)
        assert dto.incidents[0].maintenance_status == "scheduled"
        assert dto.incidents[0].updates[0].publish_locations == ["riotclient"]

        dumped = dto.model_dump(by_alias=True)
        assert dumped["incidents"][0]["maintenanceStatus"] == "scheduled"
        assert dumped["incidents"][0]["updates"][0]["publishLocations"] == ["riotclient"]
