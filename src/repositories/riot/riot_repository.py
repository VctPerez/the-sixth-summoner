import asyncio
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
        return AccountDto.model_validate(data)

    async def get_account_by_puuid(self, puuid: str) -> AccountDto:
        data = await self.provider.get_account_by_puuid(puuid)
        return AccountDto.model_validate(data)

    async def get_account_by_access_token(self, access_token: str) -> AccountDto:
        data = await self.provider.get_account_by_access_token(access_token)
        return AccountDto.model_validate(data)

    async def get_all_champion_mastery_entries_by_puuid(self, puuid: str) -> List[ChampionMasteryDto]:
        data = await self.provider.get_all_champion_mastery_entries_by_puuid(puuid)
        return [ChampionMasteryDto.model_validate(entry) for entry in data]

    async def get_champion_mastery_entry_by_champion_id(self, puuid: str, champion_id: int) -> ChampionMasteryDto:
        data = await self.provider.get_champion_mastery_entry_by_champion_id(puuid, champion_id)
        return ChampionMasteryDto.model_validate(data)

    async def get_all_league_entries(self, queue: Queue, tier: Tier, division: Division) -> List[LeagueEntryDto]:
        data = await self.provider.get_all_league_entries(queue, tier, division)
        return [LeagueEntryDto.model_validate(entry) for entry in data]

    async def get_platform_status(self) -> PlatformDataDto:
        data = await self.provider.get_platform_status()
        return PlatformDataDto.model_validate(data)

    async def get_match_ids_by_puuid(self, puuid: str, count: int = 20) -> List[str]:
        return await self.provider.get_match_ids_by_puuid(puuid, count)

    async def get_match_details(self, match_id: str) -> MatchDto:
        match_task = self.provider.get_match_details(match_id)
        timeline_task = self.get_match_timeline_by_match_id(match_id)

        match_data, match_timeline = await asyncio.gather(match_task, timeline_task)

        match_data["timeline"] = match_timeline.model_dump()
        return MatchDto.model_validate(match_data)

    async def get_match_timeline_by_match_id(self, match_id: str) -> MatchTimelineDto:
        data = await self.provider.get_match_timeline_by_match_id(match_id)
        return MatchTimelineDto.model_validate(data)

    async def get_current_game_info_by_summoner_id(self, summoner_puuid: str) -> CurrentGameInfoDto:
        data = await self.provider.get_current_game_info_by_summoner_id(summoner_puuid)
        return CurrentGameInfoDto.model_validate(data)

    async def get_summoner_by_puuid(self, puuid: str) -> SummonerDto:
        data = await self.provider.get_summoner_by_puuid(puuid)
        return SummonerDto.model_validate(data)

    async def get_summoner_by_access_token(self, access_token: str) -> SummonerDto:
        data = await self.provider.get_summoner_by_access_token(access_token)
        return SummonerDto.model_validate(data)
