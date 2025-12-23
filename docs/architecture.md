# Architecture

## Overview

This repository implements the **Monthly Weather Trends** feature as a two-tier web application:

- **Backend**: Python 3.12 + FastAPI service that loads a local CSV dataset and exposes read-only JSON APIs.
- **Frontend**: Next.js (App Router) single-page dashboard that fetches backend data and renders charts + UI controls.

Core goals:

- Deterministic, reproducible aggregations.
- Clear SOLID boundaries between infrastructure, domain logic, and web/API layers.
- High test confidence with enforced coverage.

---

## Backend Architecture (FastAPI)

### Responsibilities

- Load weather observations from `src/main/resources/WeatherData.csv`.
- Select the **latest full year** in the dataset.
- Compute:
  - Monthly averages (temperature, humidity) for the selected year.
  - Monthly trend for a selected month: daily aggregates + most common condition.
- Expose versioned APIs under `/api/v1/*`.

### Layering / Design

- **Infrastructure** (`backend/src/infrastructure`)
  - `csv_loader.py`: Reads CSV using pandas; handles file/parse failures with logging and error propagation.
- **Domain models** (`backend/src/domain/models`)
  - Typed objects representing observations and aggregations (e.g., `WeatherObservation`, `MonthlySummary`, `DailyAggregate`, `MonthlyTrend`).
- **Domain services** (`backend/src/domain/services`)
  - `yearly_aggregation_service.py`: monthly averages for the latest full year.
  - `monthly_trend_service.py`: per-month daily aggregates + most common condition, deterministic tie-breaking.
- **API layer** (`backend/src/api/v1`)
  - Endpoint modules (e.g., `yearly_summary.py`, `monthly_trend.py`) translate between HTTP/DTOs and domain services.
  - DTOs live in `backend/src/api/v1/dtos`.
- **App entrypoint** (`backend/src/main.py`)
  - FastAPI app wiring and router inclusion.

### Backend API Surface (high level)

- `GET /api/v1/yearly-summary`
  - Returns `year`, `months[]`, and metadata (`total_observation_count`, `months_with_data`).
- `GET /api/v1/monthly-trend?month={1..12}`
  - Returns `year`, `month`, `daily_aggregates[]`, and `most_common_condition`.
- `GET /api/v1/health`
  - Basic health check.

---

## Frontend Architecture (Next.js)

### Responsibilities

- Load yearly summary on page load.
- Render:
  - Yearly averages charts (temperature + humidity).
  - Month selector based on availability.
  - Monthly trend view for selected month.
  - Data assumptions/coverage metadata.
- Provide clear error/no-data UI states.

### Key Modules

- `frontend/app/page.tsx`
  - Main dashboard route. Orchestrates data loading and conditional rendering.
- `frontend/lib/apiClient.ts`
  - Typed fetch wrapper for backend endpoints.
  - Supports optional `NEXT_PUBLIC_API_BASE_URL`.
- `frontend/components/*`
  - `YearlyAveragesChart.tsx`: chart.js rendering for monthly averages.
  - `MonthSelector.tsx`: month dropdown; disabled when no months are available.
  - `MonthlyTrendView.tsx`: fetches and shows daily aggregates + most common condition.
  - `DataAssumptions.tsx`: explains dataset source, selected year, and coverage.

---

## Project Layout

```text
.
├── backend/
│   ├── src/
│   │   ├── api/v1/
│   │   ├── domain/
│   │   ├── infrastructure/
│   │   └── main.py
│   └── tests/
│       ├── unit/
│       └── integration/
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── tests/
│       ├── unit/
│       └── e2e/
├── specs/
│   └── 001-monthly-weather-trends/
│       ├── spec.md
│       ├── plan.md
│       ├── contracts/
│       ├── tasks.md
│       └── quickstart.md
└── docs/
    └── architecture.md
```

---

## Testing Summary

### Backend (pytest)

- **Unit tests**: validate domain aggregation logic.
- **Integration tests**: validate FastAPI endpoints and DTO responses.
- **Coverage enforcement**: pytest is configured to fail below **90%** coverage.

Typical commands (from `backend/`):

- `uv run pytest`

### Frontend (Jest + Testing Library)

- **Unit/component tests** for UI components and `apiClient`.
- **Coverage enforcement**: Jest coverage thresholds are enforced (≥90% on lines/statements).

Typical commands (from `frontend/`):

- `npm test`
- `npm run test:coverage`

### E2E (Playwright)

- Primary UI flows are tested with mocked API responses.

Typical commands (from `frontend/`):

- `npx playwright test`

---

## Static Code Analysis Summary

The following repo-supported static checks were executed:

### Frontend

- **ESLint (Next.js)**: `npm run lint`
  - Result: **PASS** (no warnings/errors)
- **TypeScript typecheck**: `npx tsc --noEmit`
  - Result: **PASS**

### Backend

- **Python bytecode compilation check**: `uv run python -m compileall -q src`
  - Result: **PASS**

Notes:

- The frontend lint run previously flagged an unescaped apostrophe in JSX (`react/no-unescaped-entities`); this was corrected and lint now passes cleanly.

### Size & Complexity (LOC and approximate cyclomatic indicators)

The following metrics are lightweight and dependency-free:

- **LOC**: count of non-blank, non-comment lines.
- **Complexity (approx)**: `1 + count(branching / boolean keywords)`.
  - Python keywords counted: `if`, `elif`, `for`, `while`, `case`, `except`, `and`, `or`.
  - TypeScript/TSX keywords counted: `if`, `for`, `while`, `switch`, `case`, `catch`, `&&`, `||`.

#### LOC + Complexity by module

| Module | Files | LOC (non-blank, non-comment) | Complexity (approx) |
|--------|------:|-----------------------------:|--------------------:|
| backend/src/__init__.py | 1 | 0 | 1 |
| backend/src/api | 6 | 139 | 38 |
| backend/src/domain | 5 | 169 | 37 |
| backend/src/infrastructure | 2 | 60 | 11 |
| backend/src/main.py | 1 | 29 | 5 |
| frontend/app | 2 | 69 | 7 |
| frontend/components | 4 | 251 | 18 |
| frontend/lib | 1 | 45 | 5 |

#### Most complex backend files (approx)

| Complexity (approx) | LOC | File |
|--------------------:|----:|------|
| 15 | 60 | `backend/src/domain/services/monthly_trend_service.py` |
| 12 | 71 | `backend/src/domain/services/yearly_aggregation_service.py` |
| 11 | 54 | `backend/src/api/v1/monthly_trend.py` |
| 11 | 52 | `backend/src/api/v1/yearly_summary.py` |
| 10 | 60 | `backend/src/infrastructure/csv_loader.py` |

#### Most complex frontend files (approx)

| Complexity (approx) | LOC | File |
|--------------------:|----:|------|
| 9 | 74 | `frontend/components/MonthlyTrendView.tsx` |
| 6 | 54 | `frontend/app/page.tsx` |
| 5 | 45 | `frontend/lib/apiClient.ts` |
| 4 | 87 | `frontend/components/YearlyAveragesChart.tsx` |
| 3 | 52 | `frontend/components/MonthSelector.tsx` |
