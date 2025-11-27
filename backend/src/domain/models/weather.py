"""Domain models for weather observations and aggregates."""

from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional


@dataclass(frozen=True)
class WeatherObservation:
    """Single raw weather observation."""

    timestamp: datetime
    temperature: float
    humidity: float
    condition: str

    @property
    def date(self) -> date:
        return self.timestamp.date()


@dataclass(frozen=True)
class MonthlySummary:
    """Aggregated monthly averages for a specific year."""

    year: int
    month: int  # 1–12
    avg_temperature: Optional[float]
    avg_humidity: Optional[float]
    observation_count: int


@dataclass(frozen=True)
class DailyAggregate:
    """Aggregated daily values within a month."""

    year: int
    month: int  # 1–12
    day: int    # 1–31
    avg_temperature: Optional[float]
    avg_humidity: Optional[float]
    observation_count: int


@dataclass(frozen=True)
class MonthlyTrend:
    """Trend data for a selected month: daily aggregates + most common condition."""

    year: int
    month: int  # 1–12
    daily_aggregates: List[DailyAggregate]
    most_common_condition: Optional[str]
