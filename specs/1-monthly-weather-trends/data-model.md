# Data Model: Monthly Weather Trends

**Feature**: Monthly Weather Trends  
**Branch**: `1-monthly-weather-trends`

## Entities

### WeatherObservation

Represents a single raw record from `WeatherData.csv`.

- **Fields**:
  - `id` (optional/internal): unique identifier for the observation (e.g., row index).
  - `timestamp` (datetime): exact time of the observation.
  - `date` (date): calendar date derived from `timestamp`.
  - `temperature` (float): recorded temperature in degrees (unit as provided by data; assumed Celsius unless clarified otherwise).
  - `humidity` (float): recorded relative humidity percentage (0–100).
  - `condition` (string): categorical weather condition label (e.g., `"clear"`, `"cloudy"`, `"rain"`).

- **Validation rules**:
  - `humidity` must be within [0, 100]; values outside this range are treated as invalid and either corrected (if obvious) or excluded from aggregates.
  - `temperature` must be a finite numeric value; non-numeric or NaN values are excluded from aggregates.
  - `timestamp` must be parseable as a valid datetime; invalid rows are skipped or logged as errors.

### MonthlySummary

Represents aggregated data for a specific month within a specific year.

- **Fields**:
  - `year` (int): the calendar year of the summary.
  - `month` (int): the calendar month as 1–12.
  - `avg_temperature` (float | null): average temperature over all valid observations in that month.
  - `avg_humidity` (float | null): average humidity over all valid observations in that month.
  - `observation_count` (int): number of valid observations included in the averages.

- **Rules**:
  - Summaries are computed only for the **latest full year** detected in the dataset.
  - A month may be included even if `observation_count` is small (≥1), in which case averages are based on available observations and this should be documented in the UI.

### DailyAggregate

Represents aggregated data for a specific day within a month.

- **Fields**:
  - `year` (int)
  - `month` (int, 1–12)
  - `day` (int, 1–31)
  - `avg_temperature` (float | null)
  - `avg_humidity` (float | null)
  - `observation_count` (int)

- **Rules**:
  - Derived from `WeatherObservation` records grouped by date.
  - Used as the basis for trend charts within a month.

### MonthlyTrend

Represents the trend view for a selected month.

- **Fields**:
  - `year` (int)
  - `month` (int, 1–12)
  - `daily_aggregates` (list[DailyAggregate]): ordered by date ascending.
  - `most_common_condition` (string | null): most frequently occurring `condition` value in that month (ties resolved deterministically, e.g., by alphabetical order).

- **Rules**:
  - `daily_aggregates` must be deterministic given the same input data.
  - If there are no valid observations for the month, `daily_aggregates` is empty and `most_common_condition` is null.

## Relationships

- A `WeatherObservation` belongs to exactly one (`year`, `month`, `day`).
- A `MonthlySummary` aggregates many `WeatherObservation` records for a given (`year`, `month`).
- A `DailyAggregate` aggregates many `WeatherObservation` records for a given (`year`, `month`, `day`).
- A `MonthlyTrend` consists of many `DailyAggregate` records for a specific (`year`, `month`).

## Assumptions

- All data for this feature comes from a single CSV file `src/main/resources/WeatherData.csv`.
- Timezone handling is not critical for this feature; timestamps are interpreted in a consistent local or UTC timezone as configured at implementation time.
- Units (e.g., Celsius vs Fahrenheit) will be treated consistently across the dataset and surfaced in the UI.
