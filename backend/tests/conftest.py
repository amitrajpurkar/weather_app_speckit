"""Shared pytest configuration and fixtures."""

import pandas as pd
import pytest
from datetime import datetime
from pathlib import Path

from src.domain.models.weather import WeatherObservation
from src.infrastructure.csv_loader import load_weather_data


@pytest.fixture
def sample_csv_path(tmp_path: Path) -> Path:
    """Create a temporary WeatherData.csv with a few rows of sample data."""
    csv_path = tmp_path / "WeatherData.csv"
    data = [
        {
            "timestamp": "2024-01-01 08:00",
            "temperature": 5.0,
            "humidity": 70.0,
            "condition": "clear",
        },
        {
            "timestamp": "2024-01-01 14:00",
            "temperature": 7.5,
            "humidity": 68.0,
            "condition": "clear",
        },
        {
            "timestamp": "2024-01-02 08:00",
            "temperature": 4.5,
            "humidity": 72.0,
            "condition": "cloudy",
        },
        {
            "timestamp": "2024-02-01 08:00",
            "temperature": 6.0,
            "humidity": 65.0,
            "condition": "rain",
        },
    ]
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)
    return csv_path


@pytest.fixture
def sample_observations() -> list[WeatherObservation]:
    """A small list of WeatherObservation objects for testing domain logic."""
    return [
        WeatherObservation(
            timestamp=datetime(2024, 1, 1, 8, 0),
            temperature=5.0,
            humidity=70.0,
            condition="clear",
        ),
        WeatherObservation(
            timestamp=datetime(2024, 1, 1, 14, 0),
            temperature=7.5,
            humidity=68.0,
            condition="clear",
        ),
        WeatherObservation(
            timestamp=datetime(2024, 1, 2, 8, 0),
            temperature=4.5,
            humidity=72.0,
            condition="cloudy",
        ),
        WeatherObservation(
            timestamp=datetime(2024, 2, 1, 8, 0),
            temperature=6.0,
            humidity=65.0,
            condition="rain",
        ),
    ]
