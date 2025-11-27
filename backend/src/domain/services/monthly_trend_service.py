"""Service to compute monthly trend (daily aggregates + most common condition)."""

from collections import Counter, defaultdict
from typing import List, Optional

import pandas as pd

from ..models.weather import DailyAggregate, MonthlyTrend, WeatherObservation


def compute_monthly_trend(
    observations: List[WeatherObservation],
) -> Optional[MonthlyTrend]:
    """
    Compute daily aggregates and most common condition for a given month.

    Parameters
    ----------
    observations: List[WeatherObservation]
        Raw observations for a specific month/year.

    Returns
    -------
    Optional[MonthlyTrend]
        None if no observations are provided; otherwise a populated MonthlyTrend.
    """
    if not observations:
        return None

    year = observations[0].date.year
    month = observations[0].date.month

    # Group by day and compute daily averages
    day_data = defaultdict(lambda: {"temps": [], "humidities": []})
    conditions_by_day = defaultdict(list)

    for obs in observations:
        day = obs.date.day
        day_data[day]["temps"].append(obs.temperature)
        day_data[day]["humidities"].append(obs.humidity)
        conditions_by_day[day].append(obs.condition)

    daily_aggregates = []
    for day in range(1, 32):
        temps = day_data[day]["temps"]
        humidities = day_data[day]["humidities"]
        if temps:  # at least one observation for this day
            avg_temp = sum(temps) / len(temps)
            avg_hum = sum(humidities) / len(humidities)
            daily_aggregates.append(
                DailyAggregate(
                    year=year,
                    month=month,
                    day=day,
                    avg_temperature=avg_temp,
                    avg_humidity=avg_hum,
                    observation_count=len(temps),
                )
            )
        else:
            # No data for this day
            daily_aggregates.append(
                DailyAggregate(
                    year=year,
                    month=month,
                    day=day,
                    avg_temperature=None,
                    avg_humidity=None,
                    observation_count=0,
                )
            )

    # Determine most common condition across the month
    all_conditions = [obs.condition for obs in observations if obs.condition]
    most_common = None
    if all_conditions:
        counter = Counter(all_conditions)
        max_count = max(counter.values())
        # Resolve ties deterministically by alphabetical order
        candidates = [cond for cond, cnt in counter.items() if cnt == max_count]
        most_common = min(candidates)

    return MonthlyTrend(
        year=year,
        month=month,
        daily_aggregates=daily_aggregates,
        most_common_condition=most_common,
    )
