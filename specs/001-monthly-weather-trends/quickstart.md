# Quickstart: Monthly Weather Trends

This guide covers running the backend and frontend locally, as well as running the test suites and viewing coverage.

## Prerequisites

- Python 3.12
- `uv` installed
- Node.js 20+

## Backend (FastAPI)

### Install

From `backend/`:

```sh
uv venv
uv pip install -e ".[dev]"
```

### Run

From `backend/`:

```sh
uv run uvicorn src.main:app --reload --port 8000
```

Health check:

```sh
curl http://localhost:8000/api/v1/health
```

### Run tests + coverage

From `backend/`:

```sh
uv run pytest
```

Coverage is enforced by pytest configuration (≥90%).

## Frontend (Next.js)

### Install

From `frontend/`:

```sh
npm ci
```

### Run

From `frontend/`:

```sh
npm run dev
```

Open:

- http://localhost:3000

### Configure backend base URL (optional)

By default the frontend uses `NEXT_PUBLIC_API_BASE_URL` if set; otherwise it calls relative paths.

Example:

```sh
export NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### Run unit tests

From `frontend/`:

```sh
npm test
```

### Run unit tests with coverage

From `frontend/`:

```sh
npm run test:coverage
```

Coverage is enforced by Jest configuration (≥90%).

### Run E2E tests (Playwright)

From `frontend/`:

```sh
npx playwright install
npx playwright test
```

## What data is used?

The backend reads from:

- `src/main/resources/WeatherData.csv`

and automatically selects the latest full year for yearly summaries and monthly trends.
