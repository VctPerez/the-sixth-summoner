from src.schemas.riot.match.match_dto import MatchDto, MatchInfoDto, MetadataDto, ParticipantDto
from src.services.riot.ml.riot_feature_parser import RiotFeatureParser


def _build_participant(
        *,
        puuid: str,
        participant_id: int,
        team_id: int,
        champion_id: int,
        win: bool,
        kills: int,
) -> ParticipantDto:
    return ParticipantDto.model_construct(
        puuid=puuid,
        participant_id=participant_id,
        team_id=team_id,
        champion_id=champion_id,
        win=win,
        kills=kills,
        deaths=2,
        assists=5,
        gold_earned=11000,
        total_damage_dealt_to_champions=22000,
        vision_score=30,
        total_minions_killed=150,
        neutral_minions_killed=20,
    )


def _build_match(match_id: str, game_start_timestamp: int, participants: list[ParticipantDto]) -> MatchDto:
    metadata = MetadataDto.model_construct(
        data_version="2",
        match_id=match_id,
        participants=[participant.puuid for participant in participants],
    )
    info = MatchInfoDto.model_construct(
        game_start_timestamp=game_start_timestamp,
        game_duration=1800,
        queue_id=420,
        participants=participants,
    )
    return MatchDto.model_construct(metadata=metadata, info=info, timeline=None)


def test_build_dataset_creates_rows_and_player_history():
    parser = RiotFeatureParser()

    older_match = _build_match(
        match_id="EUW1_1",
        game_start_timestamp=100,
        participants=[
            _build_participant(
                puuid="same-player",
                participant_id=1,
                team_id=100,
                champion_id=266,
                win=True,
                kills=10,
            ),
            _build_participant(
                puuid="other-player",
                participant_id=2,
                team_id=200,
                champion_id=103,
                win=False,
                kills=2,
            ),
        ],
    )

    newer_match = _build_match(
        match_id="EUW1_2",
        game_start_timestamp=200,
        participants=[
            _build_participant(
                puuid="same-player",
                participant_id=1,
                team_id=100,
                champion_id=157,
                win=False,
                kills=3,
            ),
            _build_participant(
                puuid="other-player-2",
                participant_id=2,
                team_id=200,
                champion_id=81,
                win=True,
                kills=7,
            ),
        ],
    )

    dataset = parser.build_dataset([newer_match, older_match])

    assert dataset.feature_names == parser.feature_names
    assert len(dataset.rows) == 4

    rows_by_match_and_player = {(row.match_id, row.puuid): row for row in dataset.rows}

    first_row = rows_by_match_and_player[("EUW1_1", "same-player")]
    assert first_row.prior_matches == 0
    assert first_row.prior_win_rate == 0.0

    second_row = rows_by_match_and_player[("EUW1_2", "same-player")]
    assert second_row.prior_matches == 1
    assert second_row.prior_win_rate == 1.0


def test_build_dataset_calculates_team_kill_share():
    parser = RiotFeatureParser()
    match = _build_match(
        match_id="EUW1_3",
        game_start_timestamp=300,
        participants=[
            _build_participant(
                puuid="player-a",
                participant_id=1,
                team_id=100,
                champion_id=222,
                win=True,
                kills=6,
            ),
            _build_participant(
                puuid="player-b",
                participant_id=2,
                team_id=100,
                champion_id=99,
                win=True,
                kills=4,
            ),
            _build_participant(
                puuid="player-c",
                participant_id=3,
                team_id=200,
                champion_id=11,
                win=False,
                kills=5,
            ),
        ],
    )

    dataset = parser.build_dataset([match])
    row = next(row for row in dataset.rows if row.puuid == "player-a")

    assert row.team_kill_share == 0.6
