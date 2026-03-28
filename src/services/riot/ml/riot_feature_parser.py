from collections import defaultdict

from src.schemas.riot.match import MatchDto
from src.schemas.riot.ml import MatchFeatureRowDto, RiotMlDatasetDto


class RiotFeatureParser:
    feature_names = [
        "champion_id",
        "team_id",
        "queue_id",
        "game_duration_seconds",
        "kills",
        "deaths",
        "assists",
        "kda_ratio",
        "gold_earned",
        "total_damage_dealt_to_champions",
        "vision_score",
        "total_cs",
        "team_kill_share",
        "prior_matches",
        "prior_win_rate",
    ]

    def build_dataset(self, matches: list[MatchDto]) -> RiotMlDatasetDto:
        ordered_matches = sorted(matches, key=lambda match: match.info.game_start_timestamp)
        rows: list[MatchFeatureRowDto] = []

        player_history: dict[str, dict[str, int]] = defaultdict(lambda: {"wins": 0, "games": 0})

        for match in ordered_matches:
            team_kills = self._compute_team_kills(match)

            for participant in match.info.participants:
                history = player_history[participant.puuid]
                prior_games = history["games"]
                prior_win_rate = history["wins"] / prior_games if prior_games else 0.0

                total_cs = participant.total_minions_killed + participant.neutral_minions_killed
                kills = participant.kills
                deaths = participant.deaths
                assists = participant.assists
                kda_ratio = (kills + assists) / max(1, deaths)
                team_total_kills = max(1, team_kills.get(participant.team_id, 0))

                rows.append(
                    MatchFeatureRowDto(
                        match_id=match.metadata.match_id,
                        puuid=participant.puuid,
                        participant_id=participant.participant_id,
                        champion_id=participant.champion_id,
                        team_id=participant.team_id,
                        queue_id=match.info.queue_id,
                        game_duration_seconds=match.info.game_duration,
                        kills=kills,
                        deaths=deaths,
                        assists=assists,
                        kda_ratio=kda_ratio,
                        gold_earned=participant.gold_earned,
                        total_damage_dealt_to_champions=participant.total_damage_dealt_to_champions,
                        vision_score=participant.vision_score,
                        total_cs=total_cs,
                        team_kill_share=kills / team_total_kills,
                        prior_matches=prior_games,
                        prior_win_rate=prior_win_rate,
                        win=participant.win,
                    )
                )

            # Update history after creating features so current match is not leaked.
            for participant in match.info.participants:
                history = player_history[participant.puuid]
                history["games"] += 1
                history["wins"] += int(participant.win)

        return RiotMlDatasetDto(feature_names=self.feature_names, rows=rows)

    @staticmethod
    def _compute_team_kills(match: MatchDto) -> dict[int, int]:
        team_kills: dict[int, int] = defaultdict(int)

        for participant in match.info.participants:
            team_kills[participant.team_id] += participant.kills

        return team_kills
