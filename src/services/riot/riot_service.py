from typing import Any, List

from src.repositories.riot.riot_repository import RiotRepository
from src.schemas.riot.accounts import AccountDto
from src.schemas.riot.champion_mastery import ChampionMasteryDto
from src.schemas.riot.league import LeagueEntryDto
from src.schemas.riot.league.league_parameters import Division, Queue, Tier
from src.schemas.riot.match import MatchDto, MatchTimelineDto
from src.schemas.riot.ml import RiotMlDatasetDto
from src.schemas.riot.spectator import CurrentGameInfoDto
from src.schemas.riot.status import PlatformDataDto
from src.schemas.riot.summoner import SummonerDto
from src.services.riot.ml.riot_ml_service import RiotMlService
from src.services.riot.ml.strategies.base_strategy import FrameworkStrategy


class RiotService:
    def __init__(self, repository: RiotRepository):
        self.repository = repository
        self.ml_service = RiotMlService(repository=repository)

    async def get_account_by_riot_id(self, game_name: str, tag_line: str) -> AccountDto:
        return await self.repository.get_account_by_riot_id(game_name, tag_line)

    async def get_account_by_puuid(self, puuid: str) -> AccountDto:
        return await self.repository.get_account_by_puuid(puuid)

    async def get_account_by_access_token(self, access_token: str) -> AccountDto:
        return await self.repository.get_account_by_access_token(access_token)

    async def get_all_champion_mastery_entries_by_puuid(self, puuid: str) -> List[ChampionMasteryDto]:
        return await self.repository.get_all_champion_mastery_entries_by_puuid(puuid)

    async def get_champion_mastery_entry_by_champion_id(self, puuid: str, champion_id: int) -> ChampionMasteryDto:
        return await self.repository.get_champion_mastery_entry_by_champion_id(puuid, champion_id)

    async def get_all_league_entries(self, queue: str, tier: str, division: str) -> List[LeagueEntryDto]:
        return await self.repository.get_all_league_entries(
            queue=Queue(queue),
            tier=Tier(tier),
            division=Division(division),
        )

    async def get_platform_status(self) -> PlatformDataDto:
        return await self.repository.get_platform_status()

    async def get_match_ids_by_puuid(self, puuid: str, count: int = 20) -> List[str]:
        return await self.repository.get_match_ids_by_puuid(puuid, count)

    async def get_match_details(self, match_id: str) -> MatchDto:
        return await self.repository.get_match_details(match_id)

    async def get_match_timeline_by_match_id(self, match_id: str) -> MatchTimelineDto:
        return await self.repository.get_match_timeline_by_match_id(match_id)

    async def get_current_game_info_by_summoner_id(self, summoner_puuid: str) -> CurrentGameInfoDto:
        return await self.repository.get_current_game_info_by_summoner_id(summoner_puuid)

    async def get_summoner_by_puuid(self, puuid: str) -> SummonerDto:
        return await self.repository.get_summoner_by_puuid(puuid)

    async def get_summoner_by_access_token(self, access_token: str) -> SummonerDto:
        return await self.repository.get_summoner_by_access_token(access_token)

    async def build_ml_dataset_from_puuid(self, puuid: str, count: int = 20) -> RiotMlDatasetDto:
        return await self.ml_service.build_dataset_from_puuid(puuid=puuid, count=count)

    async def build_framework_dataset_from_puuid(
            self,
            puuid: str,
            strategy: FrameworkStrategy,
            count: int = 20,
    ) -> Any:
        return await self.ml_service.build_framework_dataset_from_puuid(
            puuid=puuid,
            strategy=strategy,
            count=count,
        )
