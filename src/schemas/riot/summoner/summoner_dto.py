from ..base import RiotBaseDto


class SummonerDto(RiotBaseDto):
    account_id: str
    profile_icon_id: int
    revision_date: int
    name: str
    id: str
    puuid: str
    summoner_level: int
