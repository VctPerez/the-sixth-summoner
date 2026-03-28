from src.schemas.riot.base import RiotBaseDto


class MatchFeatureRowDto(RiotBaseDto):
    match_id: str
    puuid: str
    participant_id: int
    champion_id: int
    team_id: int
    queue_id: int
    game_duration_seconds: int
    kills: int
    deaths: int
    assists: int
    kda_ratio: float
    gold_earned: int
    total_damage_dealt_to_champions: int
    vision_score: int
    total_cs: int
    team_kill_share: float
    prior_matches: int
    prior_win_rate: float
    win: bool

    def to_feature_vector(self, feature_names: list[str]) -> list[float]:
        return [float(getattr(self, feature_name)) for feature_name in feature_names]


class RiotMlDatasetDto(RiotBaseDto):
    feature_names: list[str]
    target_name: str = "win"
    rows: list[MatchFeatureRowDto]

    def to_xy(self) -> tuple[list[list[float]], list[int]]:
        x_data = [row.to_feature_vector(self.feature_names) for row in self.rows]
        y_data = [int(row.win) for row in self.rows]
        return x_data, y_data
