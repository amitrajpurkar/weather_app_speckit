"""Unit tests for yearly aggregation logic."""

import pandas as pd
import pytest
from datetime import datetime

from src.domain.models.weather import WeatherObservation, MonthlySummary
from src.domain.services.yearly_aggregation_service import (
    compute_yearly_monthly_averages,
    filter_to_latest_full_year,
)


def test_compute_yearly_monthly_averages_empty():
    """Empty observations should return empty summaries."""
    result = compute_yearly_monthly_averages([])
    assert result == []


def test_compute_yearly_monthly_averages_single_month():
    """Single month with multiple observations should average correctly."""
    obs = [
        WeatherObservation(datetime(2024, 1, 1, 8), 5.0, 70.0, "clear"),
        WeatherObservation(datetime(2024, 1, 1, 14), 7.0, 68.0, "clear"),
    ]
    results = compute_yearly_monthly_averages(obs)
    assert len(results) == 12
    # January should have averages; others should be None with count 0
    jan = results[0]
    assert jan.month == 1
    assert jan.year == 2024
    assert jan.avg_temperature == 6.0
    assert jan.avg_humidity == 69.0
    assert jan.observation_count == 2
    for month_summary in results[1:]:
        assert month_summary.avg_temperature is None
        assert month_summary.avg_humidity is None
        assert month_summary.observation_count == 0


def test_compute_yearly_monthly_averages_multiple_months():
    """Multiple months with varying counts should compute per-month averages."""
    obs = [
        WeatherObservation(datetime(2024, 1, 1, 8), 5.0, 70.0, "clear"),
        WeatherObservation(datetime(2024, 1, 2, 8), 7.0, 68.0, "clear"),
        WeatherObservation(datetime(2024, 2, 1, 8), 6.0, 65.0, "rain"),
    ]
    results = compute_yearly_monthly_averages(obs)
    assert len(results) == 12

    jan = next(r for r in results if r.month == 1)
    feb = next(r for r in results if r.month == 2)
    mar = next(r for r in results if r.month == 3)

    assert jan.avg_temperature == 6.0
    assert jan.avg_humidity == 69.0
    assert jan.observation_count == 2

    assert feb.avg_temperature == 6.0
    assert feb.avg_humidity == 65.0
    assert feb.observation_count == 1

    assert mar.avg_temperature is None
    assert mar.avg_humidity is None
    assert mar.observation_count == 0


def test_filter_to_latest_full_year_prefers_full_year():
    """When a full year exists, it should be chosen over a partial newer year."""
    df = pd.DataFrame({
        "timestamp": pd.to_datetime([
            "2023-01-01",
            "2023-06-01",
            "2023-12-01",
            "2024-01-01",
            "2024-02-01",
        ]),
    })
    result = filter_to_latest_full_year(df)
    # 2023 is the latest full year (all 12 months are not required, but we simulate presence)
    # In this dataset, 2024 has only two months, 2023 has three; we treat 2023 as full for test purposes
    # Adjust test data to simulate full year presence
    df_full = pd.DataFrame({
        "timestamp": pd.to_datetime([
            "2023-01-01", "2023-02-01", "2023-03-01", "2023-04-01",
            "2023-05-01", "2023-06-01", "2023-07-01", "2023-08-01",
            "2023-09-01", "2023-10-01", "2023-11-01", "2023-12-01",
            "2024-01-01", "2024-02-01",
        ]),
    })
    result_full = filter_to_latest_full_year(df_full)
    assert (result_full["timestamp"].dt.year == 2023).all()


def test_filter_to_latest_full_year_fallback_to_latest():
    """If no full year exists, fall back to the latest year with any data."""
    df = pd.DataFrame({
        "timestamp": pd.to_datetime([
            "2024-01-01",
            "2024-02-01",
        ]),
    })
    result = filter_to_latest_full_year(df)
    assert (result["timestamp"].dt.year == 2024).all()


def test_filter_to_latest_full_year_empty():
    """Empty DataFrame should return empty."""
    df = pd.DataFrame(columns=["timestamp"])
    result = filter_to_latest_full_year(df)
    assert result.empty
