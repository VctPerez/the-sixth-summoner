from ..base import RiotBaseDto


class MiniSeriesDto(RiotBaseDto):
    losses: int
    progress: str
    target: int
    wins: int


class LeagueEntryDto(RiotBaseDto):
    league_id: str
    summoner_id: str
    summoner_name: str
    queue_type: str
    tier: str
    rank: str
    league_points: int
    wins: int
    losses: int
    hot_streak: bool
    veteran: bool
    fresh_blood: bool
    inactive: bool
    mini_series: MiniSeriesDto | None = None
