"""Infrastructure component to load WeatherData.csv using pandas."""

import logging
import os
from pathlib import Path

import pandas as pd


logger = logging.getLogger(__name__)


def resolve_weather_csv_path() -> Path:
    configured = os.environ.get("WEATHER_CSV_PATH")
    if configured:
        return Path(configured)

    cwd = Path.cwd().resolve()
    candidates = [
        # If uvicorn is started from backend/
        cwd / ".." / "src" / "main" / "resources" / "WeatherData.csv",
        # If uvicorn is started from backend/src/
        cwd / ".." / ".." / "src" / "main" / "resources" / "WeatherData.csv",
        # If uvicorn is started from repo root
        cwd / "src" / "main" / "resources" / "WeatherData.csv",
    ]

    for p in candidates:
        if p.is_file():
            return p

    # Final fallback: walk upwards from cwd
    for parent in [cwd, *cwd.parents]:
        candidate = parent / "src" / "main" / "resources" / "WeatherData.csv"
        if candidate.is_file():
            return candidate

    # Nothing found; return the most likely candidate for error messaging
    return candidates[0]


def load_weather_data(csv_path: Path) -> pd.DataFrame:
    """
    Load weather data from the given CSV file.

    Expected columns (normalized): timestamp, temperature, humidity, condition.
    Also supports the canonical WeatherData.csv schema:
      - Date/Time -> timestamp
      - Temp_C -> temperature
      - Rel Hum_% -> humidity
      - Weather -> condition
    Returns a pandas DataFrame with parsed datetime index.
    """
    if not csv_path.is_file():
        logger.error("Weather CSV not found", extra={"csv_path": str(csv_path)})
        raise FileNotFoundError(f"Weather CSV not found at {csv_path}")

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        logger.exception("Failed to read weather CSV", extra={"csv_path": str(csv_path)})
        raise

    # Normalize column names (support both the internal normalized schema and the raw CSV schema)
    canonical_to_normalized = {
        "Date/Time": "timestamp",
        "Temp_C": "temperature",
        "Rel Hum_%": "humidity",
        "Weather": "condition",
    }
    if not {"timestamp", "temperature", "humidity", "condition"}.issubset(df.columns):
        df = df.rename(columns={k: v for k, v in canonical_to_normalized.items() if k in df.columns})

    # Basic validation and parsing
    required_columns = {"timestamp", "temperature", "humidity", "condition"}
    missing = required_columns - set(df.columns)
    if missing:
        logger.error(
            "CSV missing required columns",
            extra={
                "csv_path": str(csv_path),
                "missing_columns": sorted(missing),
                "available_columns": list(df.columns),
            },
        )
        raise ValueError(f"CSV missing required columns: {missing}")

    # Parse timestamps and filter invalid rows
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    before = len(df)
    df = df.dropna(subset=["timestamp"])
    dropped = before - len(df)
    if dropped:
        logger.warning(
            "Dropped rows with invalid timestamps",
            extra={"csv_path": str(csv_path), "dropped_rows": dropped},
        )

    # Ensure numeric columns are numeric; coerce errors to NaN
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df["humidity"] = pd.to_numeric(df["humidity"], errors="coerce")

    # Drop rows where temperature or humidity could not be parsed
    before = len(df)
    df = df.dropna(subset=["temperature", "humidity"])
    dropped = before - len(df)
    if dropped:
        logger.warning(
            "Dropped rows with non-numeric temperature/humidity",
            extra={"csv_path": str(csv_path), "dropped_rows": dropped},
        )

    # Filter out-of-range humidity values (0–100%)
    before = len(df)
    df = df[(df["humidity"] >= 0) & (df["humidity"] <= 100)]
    dropped = before - len(df)
    if dropped:
        logger.warning(
            "Dropped rows with out-of-range humidity",
            extra={"csv_path": str(csv_path), "dropped_rows": dropped},
        )

    # Ensure condition is a string, replace NaN with empty string
    df["condition"] = df["condition"].fillna("").astype(str)

    logger.info(
        "Loaded weather CSV",
        extra={"csv_path": str(csv_path), "row_count": len(df)},
    )
    return df.sort_values("timestamp").reset_index(drop=True)
