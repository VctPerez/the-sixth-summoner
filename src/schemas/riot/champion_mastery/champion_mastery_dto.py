from ..base import RiotBaseDto


class ChampionMasteryDto(RiotBaseDto):
    puuid: str
    champion_id: int
    champion_level: int
    champion_points: int
    last_play_time: int
    champion_points_since_last_level: int
    champion_points_until_next_level: int
    chest_granted: bool
    tokens_earned: int
    summoner_id: str
