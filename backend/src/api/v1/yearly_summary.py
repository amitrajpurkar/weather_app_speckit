"""API endpoint for yearly monthly averages."""

from typing import List

from fastapi import APIRouter

from ...domain.models.weather import MonthlySummary
from ...domain.services.yearly_aggregation_service import (
    compute_yearly_monthly_averages,
    filter_to_latest_full_year,
)
from ...infrastructure.csv_loader import load_weather_data
from ..dtos.yearly_summary_dtos import YearlySummaryResponse, MonthlySummaryDto

router = APIRouter()


def _df_to_observations(df: "pd.DataFrame") -> List["WeatherObservation"]:
    """Convert pandas DataFrame rows to WeatherObservation objects."""
    from ...domain.models.weather import WeatherObservation
    return [
        WeatherObservation(
            timestamp=row["timestamp"],
            temperature=row["temperature"],
            humidity=row["humidity"],
            condition=row["condition"],
        )
        for _, row in df.iterrows()
    ]


@router.get("/yearly-summary", response_model=YearlySummaryResponse)
def get_yearly_summary() -> YearlySummaryResponse:
    """
    Return monthly average temperature and humidity for the latest full year.
    """
    # Load and filter data
    df = load_weather_data(
        Path(__file__).parent.parent.parent.parent / "src" / "main" / "resources" / "WeatherData.csv"
    )
    df_latest = filter_to_latest_full_year(df)

    # Convert to domain objects
    observations = _df_to_observations(df_latest)

    # Compute summaries
    summaries = compute_yearly_monthly_averages(observations)

    # Map to DTOs
    months = [
        MonthlySummaryDto(
            month=s.month,
            avg_temperature=s.avg_temperature,
            avg_humidity=s.avg_humidity,
            observation_count=s.observation_count,
        )
        for s in summaries
    ]

    year = summaries[0].year if summaries else None
    return YearlySummaryResponse(year=year, months=months)
