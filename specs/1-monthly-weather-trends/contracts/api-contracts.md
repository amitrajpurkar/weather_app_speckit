# API Contracts: Monthly Weather Trends

**Feature**: Monthly Weather Trends  
**Branch**: `1-monthly-weather-trends`

These contracts describe the JSON APIs to be implemented by the FastAPI backend.

## Base URL

- Backend base: `/api/v1`

## 1. GET `/api/v1/yearly-summary`

Return monthly average temperature and humidity for the latest full year.

### Request

- **Method**: `GET`
- **Query Parameters**: none (the backend detects the latest full year automatically from the data).

### Response

- **Status 200 OK**

```json
{
  "year": 2024,
  "months": [
    {
      "month": 1,
      "avg_temperature": 5.2,
      "avg_humidity": 72.1,
      "observation_count": 93
    }
  ]
}
```

- **Fields**:
  - `year` (int): the year used for the summary (latest full year).
  - `months` (array of `MonthlySummaryDto`): one per month that has at least one valid observation.

- **MonthlySummaryDto**:
  - `month` (int, 1–12)
  - `avg_temperature` (number | null)
  - `avg_humidity` (number | null)
  - `observation_count` (int)

### Error Responses

- **Status 404 Not Found**: no valid data available (e.g., CSV missing or fully invalid).

```json
{
  "detail": "No valid weather data available for yearly summary."
}
```

---

## 2. GET `/api/v1/monthly-trend`

Return daily aggregated temperature and humidity for a specific month in the latest full year, plus the most common weather condition.

### Request

- **Method**: `GET`
- **Query Parameters**:
  - `month` (int, required): month number 1–12.

Example:

```http
GET /api/v1/monthly-trend?month=3
```

### Response

- **Status 200 OK**

```json
{
  "year": 2024,
  "month": 3,
  "daily_aggregates": [
    {
      "day": 1,
      "avg_temperature": 7.1,
      "avg_humidity": 68.5,
      "observation_count": 3
    }
  ],
  "most_common_condition": "rain"
}
```

- **Fields**:
  - `year` (int): the year used for the trend (same as yearly summary year).
  - `month` (int): requested month.
  - `daily_aggregates` (array of `DailyAggregateDto`): one per day with at least one valid observation.
  - `most_common_condition` (string | null): most frequent condition for that month.

- **DailyAggregateDto**:
  - `day` (int, 1–31)
  - `avg_temperature` (number | null)
  - `avg_humidity` (number | null)
  - `observation_count` (int)

### Error Responses

- **Status 400 Bad Request**: invalid month value.

```json
{
  "detail": "Month must be between 1 and 12."
}
```

- **Status 404 Not Found**: no data for requested month.

```json
{
  "detail": "No data available for requested month."
}
```

## 3. Health Check (optional)

Optional simple endpoint for operational checks.

- **GET** `/api/v1/health`

```json
{
  "status": "ok"
}
```

Used by monitoring and during local development to verify the backend is running.
