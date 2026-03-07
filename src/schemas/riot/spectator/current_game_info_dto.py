from ..base import RiotBaseDto


class BannedChampionDto(RiotBaseDto):
    pick_turn: int
    champion_id: int
    team_id: int


class ObserverDto(RiotBaseDto):
    encryption_key: str


class PerksDto(RiotBaseDto):
    perk_ids: list[int]
    perk_style: int
    perk_sub_style: int


class GameCustomizationObjectDto(RiotBaseDto):
    category: str
    content: str


class CurrentGameParticipantDto(RiotBaseDto):
    champion_id: int
    perks: PerksDto
    profile_icon_id: int
    bot: bool
    team_id: int
    summoner_name: str
    summoner_id: str
    spell1_id: int
    spell2_id: int
    game_customization_objects: list[GameCustomizationObjectDto]
    riot_id: str | None = None
    puuid: str | None = None


class CurrentGameInfoDto(RiotBaseDto):
    game_id: int
    game_type: str
    game_start_time: int
    map_id: int
    game_length: int
    platform_id: str
    game_mode: str
    banned_champions: list[BannedChampionDto]
    game_queue_config_id: int | None = None
    observers: ObserverDto | None = None
    participants: list[CurrentGameParticipantDto]
