import importlib
from typing import cast

import pandas as pd
import pytest

from src.schemas.riot.ml import MatchFeatureRowDto, RiotMlDatasetDto
from src.services.riot.ml.strategies import SklearnStrategy, TorchStrategy


def _build_dataset() -> RiotMlDatasetDto:
    rows = [
        MatchFeatureRowDto(
            match_id="EUW1_1",
            puuid="p1",
            participant_id=1,
            champion_id=266,
            team_id=100,
            queue_id=420,
            game_duration_seconds=1800,
            kills=7,
            deaths=2,
            assists=8,
            kda_ratio=7.5,
            gold_earned=12000,
            total_damage_dealt_to_champions=23000,
            vision_score=24,
            total_cs=180,
            team_kill_share=0.45,
            prior_matches=3,
            prior_win_rate=0.66,
            win=True,
        ),
        MatchFeatureRowDto(
            match_id="EUW1_2",
            puuid="p2",
            participant_id=2,
            champion_id=103,
            team_id=200,
            queue_id=420,
            game_duration_seconds=1750,
            kills=2,
            deaths=7,
            assists=4,
            kda_ratio=0.85,
            gold_earned=8900,
            total_damage_dealt_to_champions=14500,
            vision_score=16,
            total_cs=140,
            team_kill_share=0.2,
            prior_matches=1,
            prior_win_rate=1.0,
            win=False,
        ),
    ]

    return RiotMlDatasetDto(feature_names=[
        "champion_id",
        "team_id",
        "queue_id",
        "kills",
        "deaths",
        "assists",
        "kda_ratio",
        "prior_matches",
        "prior_win_rate",
    ], rows=rows)


def test_sklearn_strategy_returns_dataframe_and_series():
    dataset = _build_dataset()
    strategy = SklearnStrategy()

    result = strategy.build_training_data(dataset)
    x_frame = cast(pd.DataFrame, result["x"])
    y_series = cast(pd.Series, result["y"])

    assert isinstance(x_frame, pd.DataFrame)
    assert list(x_frame.columns) == dataset.feature_names
    assert list(y_series) == [1, 0]


def test_torch_strategy_raises_when_torch_missing(monkeypatch: pytest.MonkeyPatch):
    original_import_module = importlib.import_module

    def _fake_import(name: str):
        if name == "torch":
            raise ModuleNotFoundError("torch")
        return original_import_module(name)

    monkeypatch.setattr(importlib, "import_module", _fake_import)

    dataset = _build_dataset()
    strategy = TorchStrategy()

    with pytest.raises(ImportError, match="PyTorch is not installed"):
        strategy.build_training_data(dataset)
