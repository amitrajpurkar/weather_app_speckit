"""Service to compute yearly monthly averages from raw observations."""

from collections import defaultdict
from typing import List

import pandas as pd

from ..models.weather import MonthlySummary, WeatherObservation


def compute_yearly_monthly_averages(
    observations: List[WeatherObservation],
) -> List[MonthlySummary]:
    """
    Compute average temperature and humidity for each month in the latest full year.

    Parameters
    ----------
    observations: List[WeatherObservation]
        Raw observations, assumed to be filtered to the target year.

    Returns
    -------
    List[MonthlySummary]
        One entry per month that has at least one observation.
    """
    if not observations:
        return []

    # Extract year from first observation (all should be same year after filtering)
    year = observations[0].date.year

    # Group by month and compute averages
    month_data = defaultdict(lambda: {"temps": [], "humidities": []})
    for obs in observations:
        month = obs.date.month
        month_data[month]["temps"].append(obs.temperature)
        month_data[month]["humidities"].append(obs.humidity)

    summaries = []
    for month in range(1, 13):
        temps = month_data[month]["temps"]
        humidities = month_data[month]["humidities"]
        if temps:  # at least one observation
            avg_temp = sum(temps) / len(temps)
            avg_hum = sum(humidities) / len(humidities)
            summaries.append(
                MonthlySummary(
                    year=year,
                    month=month,
                    avg_temperature=avg_temp,
                    avg_humidity=avg_hum,
                    observation_count=len(temps),
                )
            )
        else:
            # No data for this month
            summaries.append(
                MonthlySummary(
                    year=year,
                    month=month,
                    avg_temperature=None,
                    avg_humidity=None,
                    observation_count=0,
                )
            )
    return summaries


def filter_to_latest_full_year(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter the DataFrame to observations belonging to the latest full year present.

    A "full year" is defined as a year with observations for all 12 months.
    If no full year exists, the latest year with any data is used.
    """
    if df.empty:
        return df

    df["year"] = df["timestamp"].dt.year
    df["month"] = df["timestamp"].dt.month

    # Determine which years have all 12 months represented
    year_months = df.groupby("year")["month"].nunique()
    full_years = year_months[year_months == 12].index.tolist()

    if full_years:
        target_year = max(full_years)
    else:
        # Fallback: use the latest year with any data
        target_year = df["year"].max()

    return df[df["year"] == target_year].drop(columns=["year", "month"])
