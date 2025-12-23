"""Unit tests for monthly trend aggregation logic."""

from datetime import datetime

from src.domain.models.weather import WeatherObservation
from src.domain.services.monthly_trend_service import compute_monthly_trend


def test_compute_monthly_trend_daily_aggregates_and_most_common_condition(sample_observations):
    jan_obs = [o for o in sample_observations if o.date.month == 1]

    trend = compute_monthly_trend(jan_obs)
    assert trend is not None
    assert trend.year == 2024
    assert trend.month == 1

    # Only days with observations should be included
    assert [d.day for d in trend.daily_aggregates] == [1, 2]

    day1 = trend.daily_aggregates[0]
    assert day1.day == 1
    assert day1.observation_count == 2
    assert day1.avg_temperature == (5.0 + 7.5) / 2
    assert day1.avg_humidity == (70.0 + 68.0) / 2

    day2 = trend.daily_aggregates[1]
    assert day2.day == 2
    assert day2.observation_count == 1
    assert day2.avg_temperature == 4.5
    assert day2.avg_humidity == 72.0

    # clear occurs twice, cloudy once
    assert trend.most_common_condition == "clear"


def test_compute_monthly_trend_tie_breaking_is_deterministic(sample_observations):
    jan_obs = [o for o in sample_observations if o.date.month == 1]

    # Add one more 'cloudy' to create a tie: clear=2, cloudy=2
    jan_obs = jan_obs + [
        WeatherObservation(
            timestamp=datetime(2024, 1, 2, 18, 0),
            temperature=3.0,
            humidity=80.0,
            condition="cloudy",
        )
    ]

    trend = compute_monthly_trend(jan_obs)
    assert trend is not None

    # Tie should resolve alphabetically
    assert trend.most_common_condition == "clear"


def test_compute_monthly_trend_none_on_empty_input():
    assert compute_monthly_trend([]) is None
