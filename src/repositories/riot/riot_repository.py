from typing import List

from schemas.riot.league.league_parameters import Queue, Tier, Division
from src.providers.riot.riot_provider import RiotProvider
from src.schemas.riot.accounts import AccountDto
from src.schemas.riot.champion_mastery import ChampionMasteryDto
from src.schemas.riot.league import LeagueEntryDto
from src.schemas.riot.match import MatchDto, MatchTimelineDto
from src.schemas.riot.spectator import CurrentGameInfoDto
from src.schemas.riot.status import PlatformDataDto
from src.schemas.riot.summoner import SummonerDto


class RiotRepository:
    def __init__(self, provider: RiotProvider):
        self.provider = provider

    async def get_account_by_riot_id(self, game_name: str, tag_line: str) -> AccountDto:
        data = await self.provider.get_account_by_riot_id(game_name, tag_line)
        return AccountDto(**data)

    async def get_account_by_puuid(self, puuid: str) -> AccountDto:
        data = await self.provider.get_account_by_puuid(puuid)
        return AccountDto(**data)

    async def get_account_by_access_token(self, access_token: str) -> AccountDto:
        data = await self.provider.get_account_by_access_token(access_token)
        return AccountDto(**data)

    async def get_all_champion_mastery_entries_by_puuid(self, puuid: str) -> List[ChampionMasteryDto]:
        data = await self.provider.get_all_champion_mastery_entries_by_puuid(puuid)
        return [ChampionMasteryDto(**entry) for entry in data]

    async def get_champion_mastery_entry_by_champion_id(self, puuid: str, champion_id: int) -> ChampionMasteryDto:
        data = await self.provider.get_champion_mastery_entry_by_champion_id(puuid, champion_id)
        return ChampionMasteryDto(**data)

    async def get_all_league_entries(self, queue: Queue, tier: Tier, division: Division) -> List[LeagueEntryDto]:
        data = await self.provider.get_all_league_entries(queue, tier, division)
        return [LeagueEntryDto(**entry) for entry in data]

    async def get_platform_status(self) -> PlatformDataDto:
        data = await self.provider.get_platform_status()
        return PlatformDataDto(**data)

    async def get_match_ids_by_puuid(self, puuid: str, count: int = 20) -> List[str]:
        return await self.provider.get_match_ids_by_puuid(puuid, count)

    async def get_match_details(self, match_id: str) -> MatchDto:
        data = await self.provider.get_match_details(match_id)
        return MatchDto(**data)

    async def get_match_timeline_by_match_id(self, match_id: str) -> MatchTimelineDto:
        data = await self.provider.get_match_timeline_by_match_id(match_id)
        return MatchTimelineDto(**data)

    async def get_current_game_info_by_summoner_id(self, summoner_puuid: str) -> CurrentGameInfoDto:
        data = await self.provider.get_current_game_info_by_summoner_id(summoner_puuid)
        return CurrentGameInfoDto(**data)

    async def get_summoner_by_puuid(self, puuid: str) -> SummonerDto:
        data = await self.provider.get_summoner_by_puuid(puuid)
        return SummonerDto(**data)

    async def get_summoner_by_access_token(self, access_token: str) -> SummonerDto:
        data = await self.provider.get_summoner_by_access_token(access_token)
        return SummonerDto(**data)
