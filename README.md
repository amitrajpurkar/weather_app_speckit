# re-create Weather App using Spec Kit

This project demonstrates the use of Spec Kit to drive the development of a weather data analysis application.

## Features

- Monthly weather trend analysis
- Yearly average temperature and humidity charts
- Detailed monthly trend visualization
- Data aggregation and filtering
- Data validation and error handling
- Spec-driven development approach
- Test-driven development with pytest
- Comprehensive test coverage
- Clear project structure and documentation
- Modular and maintainable codebase
- Well-documented API and data models
- Easy to understand and extend
- Follows Spec Kit methodology
- Adheres to clean architecture principles

## reference..

- check the notes in [SpeckitNotes.pdf](./src/main/resources/SpeckitNotes.pdf)


## Getting Started

To run the application locally you need to start the backend (FastAPI) and the frontend (Next.js).

### Option A (recommended): two terminals

1. Backend (Terminal 1)

```sh
cd backend
uv venv
uv pip install -e ".[dev]"
uv run uvicorn src.main:app --reload --port 8000
```

2. Frontend (Terminal 2)

```sh
cd frontend
npm ci
npm run dev
```

Open:

- http://localhost:3000

### Option B: run backend + frontend from a single shell

```sh
(cd backend && uv venv && uv pip install -e ".[dev]" && uv run uvicorn src.main:app --reload --port 8000) & \
(cd frontend && npm ci && npm run dev)
```