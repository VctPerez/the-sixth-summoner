from typing import Any

from utils.http.http_client import HttpClient
from utils.http.http_method import HttpMethod


class RiotProvider:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {"X-Riot-Token": self.api_key}

        self.regional_client = HttpClient(
            base_url="https://europe.api.riotgames.com",
            default_headers=self.headers
        )
        self.platform_client = HttpClient(
            base_url="https://euw1.api.riotgames.com",
            default_headers=self.headers
        )

    def _get_headers(self):
        return {
            "X-Riot-Token": self.api_key
        }

    # -------------------------------------
    # --------- Account Endpoints ---------
    # -------------------------------------

    async def get_account_by_riot_id(self, game_name: str, tag_line: str) -> dict[str, Any]:
        return await self.regional_client.request(
            method=HttpMethod.GET,
            path="/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}",
            path_params={"game_name": game_name, "tag_line": tag_line}
        )

    async def get_account_by_puuid(self, puuid: str) -> dict[str, Any]:
        return await self.regional_client.request(
            method=HttpMethod.GET,
            path="/riot/account/v1/accounts/by-puuid/{puuid}",
            path_params={"puuid": puuid}
        )

    async def get_account_by_access_token(self, access_token: str) -> dict[str, Any]:
        return await self.regional_client.request(
            method=HttpMethod.GET,
            path="/riot/account/v1/accounts/me",
            headers={"Authorization": access_token}
        )

    # -------------------------------------
    # --------- Champion Endpoints --------
    # -------------------------------------

    async def get_all_champion_mastery_entries_by_puuid(self, puuid: str) -> list[dict[str, Any]]:
        return await self.platform_client.request(
            method=HttpMethod.GET,
            path="/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}",
            path_params={"puuid": puuid}
        )

    async def get_champion_mastery_entry_by_champion_id(self, puuid: str, champion_id: int) -> dict[str, Any]:
        return await self.platform_client.request(
            method=HttpMethod.GET,
            path="/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/by-champion/{champion_id}",
            path_params={"puuid": puuid, "champion_id": champion_id}
        )

    # -------------------------------------
    # --------- League Endpoints ----------
    # -------------------------------------

    async def get_all_league_entries(self, queue: str, tier: str, division: str) -> list[dict[str, Any]]:
        return await self.platform_client.request(
            method=HttpMethod.GET,
            path="/lol/league/v4/entries/{queue}/{tier}/{division}",
            path_params={"queue": queue, "tier": tier, "division": division}
        )

    # --------------------------------------
    # --------- Lol-Status Endpoints -------
    # --------------------------------------

    async def get_platform_status(self) -> dict[str, Any]:
        return await self.platform_client.request(
            method=HttpMethod.GET,
            path="/lol/status/v4/platform-data"
        )

    # -------------------------------------
    # --------- Match Endpoints -----------
    # -------------------------------------

    async def get_match_ids_by_puuid(self, puuid: str, count: int = 20) -> list[str]:
        return await self.regional_client.request(
            method=HttpMethod.GET,
            path="/lol/match/v5/matches/by-puuid/{puuid}/ids",
            path_params={"puuid": puuid},
            query_params={"count": count}
        )

    async def get_match_details(self, match_id: str) -> dict[str, Any]:
        return await self.regional_client.request(
            method=HttpMethod.GET,
            path="/lol/match/v5/matches/{match_id}",
            path_params={"match_id": match_id}
        )

    async def get_match_replays_by_puuid(self, puuid: str) -> dict[str, Any]:
        return await self.regional_client.request(
            method=HttpMethod.GET,
            path="/lol/match/v5/matches/by-puuid/{puuid}/replay",
            path_params={"puuid": puuid}
        )

    async def get_match_timeline_by_match_id(self, match_id: str) -> dict[str, Any]:
        return await self.regional_client.request(
            method=HttpMethod.GET,
            path="/lol/match/v5/matches/{match_id}/timeline",
            path_params={"match_id": match_id}
        )

    # -------------------------------------
    # -------- Spectator Endpoints --------
    # -------------------------------------

    async def get_current_game_info_by_summoner_id(self, summoner_puuid: str) -> dict[str, Any]:
        return await self.platform_client.request(
            method=HttpMethod.GET,
            path="/lol/spectator/v5/active-games/by-summoner/{summoner_puuid}",
            path_params={"summoner_puuid": summoner_puuid}
        )

    # -------------------------------------
    # --------- Summoner Methods ----------
    # -------------------------------------

    async def get_summoner_by_puuid(self, puuid: str) -> dict[str, Any]:
        return await self.platform_client.request(
            method=HttpMethod.GET,
            path="/lol/summoner/v4/summoners/by-puuid/{puuid}",
            path_params={"puuid": puuid}
        )

    async def get_summoner_by_access_token(self, access_token: str) -> dict[str, Any]:
        return await self.platform_client.request(
            method=HttpMethod.GET,
            path="/lol/summoner/v4/summoners/me",
            headers={"Authorization": access_token}
        )

    async def close(self):
        await self.regional_client.close()
        await self.platform_client.close()
