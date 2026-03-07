from ..base import RiotBaseDto


class MetadataTimeLineDto(RiotBaseDto):
    data_version: str
    match_id: str
    participants: list[str]


class ParticipantTimeLineDto(RiotBaseDto):
    participant_id: int
    puuid: str


class PositionDto(RiotBaseDto):
    x: int
    y: int


class MatchEventDto(RiotBaseDto):
    timestamp: int
    type: str
    participant_id: int | None = None
    item_id: int | None = None
    skill_slot: int | None = None
    level_up_type: str | None = None
    ward_type: str | None = None
    creator_id: int | None = None
    position: PositionDto | None = None
    killer_id: int | None = None
    victim_id: int | None = None
    assisting_participant_ids: list[int] | None = None
    after_id: int | None = None
    before_id: int | None = None
    gold_gain: int | None = None
    bounty: int | None = None
    kill_streak_length: int | None = None
    raw_description: str | None = None
    name: str | None = None
    level: int | None = None
    monster_type: str | None = None
    monster_sub_type: str | None = None
    team_id: int | None = None
    building_type: str | None = None
    lane_type: str | None = None
    tower_type: str | None = None
    game_id: int | None = None
    winning_team: int | None = None


class ChampionStatsDto(RiotBaseDto):
    ability_haste: int | None = None
    ability_power: int
    armor: int
    armor_pen: int | None = None
    armor_pen_percent: int | None = None
    attack_damage: int
    attack_speed: int
    bonus_armor_pen_percent: int | None = None
    bonus_magic_pen_percent: int | None = None
    cc_reduction: int
    cooldown_reduction: int
    health: int
    health_max: int
    health_regen: int
    lifesteal: int
    magic_pen: int | None = None
    magic_pen_percent: int | None = None
    magic_resist: int
    movement_speed: int
    omnivamp: int | None = None
    physical_vamp: int | None = None
    power: int
    power_max: int
    power_regen: int
    spell_vamp: int


class DamageStatsDto(RiotBaseDto):
    magic_damage_done: int
    magic_damage_done_to_champions: int
    magic_damage_taken: int
    physical_damage_done: int
    physical_damage_done_to_champions: int
    physical_damage_taken: int
    total_damage_done: int
    total_damage_done_to_champions: int
    total_damage_taken: int
    true_damage_done: int
    true_damage_done_to_champions: int
    true_damage_taken: int


class ParticipantFrameDto(RiotBaseDto):
    champion_stats: ChampionStatsDto
    current_gold: int
    damage_stats: DamageStatsDto
    gold_per_second: int
    jungle_minions_killed: int
    level: int
    minions_killed: int
    participant_id: int
    position: PositionDto
    time_enemy_spent_controlled: int
    total_gold: int
    xp: int


class MatchFrameDto(RiotBaseDto):
    events: list[MatchEventDto]
    participant_frames: dict[str, ParticipantFrameDto]
    timestamp: int


class MatchTimelineInfoDto(RiotBaseDto):
    frame_interval: int
    frames: list[MatchFrameDto]
    game_id: int | None = None
    participants: list[ParticipantTimeLineDto] | None = None


class MatchTimelineDto(RiotBaseDto):
    metadata: MetadataTimeLineDto
    info: MatchTimelineInfoDto
