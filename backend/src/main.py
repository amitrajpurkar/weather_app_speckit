"""FastAPI application entrypoint."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from .api.v1 import yearly_summary, monthly_trend
from .infrastructure.csv_loader import load_weather_data


# Cache the DataFrame at startup; in a real app you might add file watching.
_DF = None


def get_weather_df() -> "pd.DataFrame":
    """Return the cached weather DataFrame; load it once at startup."""
    global _DF
    if _DF is None:
        csv_path = Path(__file__).parent.parent.parent / "src" / "main" / "resources" / "WeatherData.csv"
        _DF = load_weather_data(csv_path)
    return _DF


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load CSV on startup to fail fast if missing/invalid
    get_weather_df()
    yield


app = FastAPI(
    title="Weather Trends API",
    description="API for monthly weather averages and trends",
    version="0.1.0",
    lifespan=lifespan,
)

# Include routers
app.include_router(yearly_summary.router, prefix="/api/v1", tags=["yearly"])
app.include_router(monthly_trend.router, prefix="/api/v1", tags=["monthly"])

# Health check
@app.get("/api/v1/health")
def health() -> dict:
    return {"status": "ok"}
