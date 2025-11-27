# Research: Monthly Weather Trends

**Feature**: Monthly Weather Trends  
**Branch**: `1-monthly-weather-trends`  
**Date**: 2025-11-27

## Decisions & Rationale

### Backend framework: FastAPI (Python 3.12)

- **Decision**: Use FastAPI as the backend web framework.
- **Rationale**:
  - First-class support for type hints and Pydantic models; aligns with SOLID/domain modeling.
  - Async-capable ASGI framework with good performance for IO-bound work (CSV reads, not heavy CPU).
  - Strong ecosystem for testing (TestClient) and OpenAPI generation.
- **Alternatives considered**:
  - **Flask**: simpler but less opinionated on typing and schema; weaker automatic OpenAPI.
  - **Django**: heavy for a small analytics service; includes ORM and features we do not need.

### Dependency and environment management: uv + Python 3.12

- **Decision**: Use Astral’s **uv** as the package/environment manager at repo root.
- **Rationale**:
  - Fast dependency resolution and reproducible environments.
  - Simplifies running backend commands (tests, app) via a single tool.
- **Alternatives considered**:
  - `pip` + `venv`: standard but slower and less ergonomic.
  - `poetry`: good dependency management but adds another layer when uv is already available.

### Data ingestion and processing: pandas

- **Decision**: Use **pandas** to read and process `WeatherData.csv`.
- **Rationale**:
  - Built-in CSV parsing with robust handling of dates and numeric types.
  - Simple APIs for grouping by year/month/day and computing aggregates.
- **Alternatives considered**:
  - Python `csv` module + manual aggregation: more boilerplate, harder to maintain.
  - `polars`: very fast but not necessary for expected data sizes and adds another dependency.

### Visualization stack: matplotlib + seaborn on backend, charting on frontend

- **Decision**: Use **matplotlib**/**seaborn** primarily for exploratory backend plotting where needed; primary user-facing charts rendered on the Next.js frontend using a JavaScript charting library (e.g., chart.js wrapper).
- **Rationale**:
  - For a web UX, client-side charts provide better interactivity and responsiveness.
  - matplotlib/seaborn can still support internal validation or static exports if required later.
- **Alternatives considered**:
  - Server-side PNG chart generation only: simpler client but less interactive; not aligned with modern web UX.

### Frontend framework: Next.js (TypeScript)

- **Decision**: Use **Next.js** (app router) with TypeScript and a single main page.
- **Rationale**:
  - Aligns with project constitution: single-page app, app directory, server components by default.
  - Good developer experience and ecosystem for testing and deployment.
- **Alternatives considered**:
  - Raw React SPA: would lose Next.js data fetching and routing conventions.

### Aggregation rules (from clarifications)

- **Decision**: When multiple years of data exist, always use the **latest full year** as the basis for yearly summaries.
- **Decision**: For a given month, compute monthly averages **whenever at least one observation exists**.
- **Decision**: Monthly trend charts use **daily aggregated values** (average temperature and humidity per day).
- **Rationale**:
  - Keeps behavior deterministic and easy to explain.
  - Ensures some signal even with sparse data, while documenting assumptions in the UI.

## Open Questions (Future Work)

- Whether to support multiple datasets or CSVs in the future (out of scope for current feature).
- Whether to add export features (CSV/PNG) for charts (not required by spec).
