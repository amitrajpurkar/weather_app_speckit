"""API endpoint for monthly trend (daily aggregates + most common condition)."""

from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from ...domain.models.weather import WeatherObservation, MonthlyTrend
from ...domain.services.monthly_trend_service import compute_monthly_trend
from ...infrastructure.csv_loader import load_weather_data
from ..dtos.monthly_trend_dtos import MonthlyTrendResponse, DailyAggregateDto

router = APIRouter()


def _df_to_observations(df: "pd.DataFrame") -> List[WeatherObservation]:
    """Convert pandas DataFrame rows to WeatherObservation objects."""
    return [
        WeatherObservation(
            timestamp=row["timestamp"],
            temperature=row["temperature"],
            humidity=row["humidity"],
            condition=row["condition"],
        )
        for _, row in df.iterrows()
    ]


@router.get("/monthly-trend", response_model=MonthlyTrendResponse)
def get_monthly_trend(month: int = Query(..., ge=1, le=12, description="Month number (1–12)")) -> MonthlyTrendResponse:
    """
    Return daily temperature/humidity aggregates and the most common weather condition for the specified month
    in the latest full year.
    """
    # Load and filter data
    df = load_weather_data(
        Path(__file__).parent.parent.parent.parent / "src" / "main" / "resources" / "WeatherData.csv"
    )
    from ...domain.services.yearly_aggregation_service import filter_to_latest_full_year
    df_latest = filter_to_latest_full_year(df)

    # Filter to requested month
    df_latest["month"] = df_latest["timestamp"].dt.month
    df_month = df_latest[df_latest["month"] == month].drop(columns=["month"])

    if df_month.empty:
        raise HTTPException(status_code=404, detail="No data available for requested month.")

    observations = _df_to_observations(df_month)
    trend = compute_monthly_trend(observations)

    if not trend:
        raise HTTPException(status_code=404, detail="No data available for requested month.")

    daily_aggregates = [
        DailyAggregateDto(
            day=d.day,
            avg_temperature=d.avg_temperature,
            avg_humidity=d.avg_humidity,
            observation_count=d.observation_count,
        )
        for d in trend.daily_aggregates
    ]

    return MonthlyTrendResponse(
        year=trend.year,
        month=trend.month,
        daily_aggregates=daily_aggregates,
        most_common_condition=trend.most_common_condition,
    )
