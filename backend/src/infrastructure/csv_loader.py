"""Infrastructure component to load WeatherData.csv using pandas."""

from pathlib import Path
from typing import List, Dict, Any

import pandas as pd


def load_weather_data(csv_path: Path) -> pd.DataFrame:
    """
    Load weather data from the given CSV file.

    Expected columns: timestamp, temperature, humidity, condition.
    Returns a pandas DataFrame with parsed datetime index.
    """
    if not csv_path.is_file():
        raise FileNotFoundError(f"Weather CSV not found at {csv_path}")

    df = pd.read_csv(csv_path)

    # Basic validation and parsing
    required_columns = {"timestamp", "temperature", "humidity", "condition"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"CSV missing required columns: {missing}")

    # Parse timestamps and filter invalid rows
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])

    # Ensure numeric columns are numeric; coerce errors to NaN
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df["humidity"] = pd.to_numeric(df["humidity"], errors="coerce")

    # Drop rows where temperature or humidity could not be parsed
    df = df.dropna(subset=["temperature", "humidity"])

    # Filter out-of-range humidity values (0–100%)
    df = df[(df["humidity"] >= 0) & (df["humidity"] <= 100)]

    # Ensure condition is a string, replace NaN with empty string
    df["condition"] = df["condition"].fillna("").astype(str)

    return df.sort_values("timestamp").reset_index(drop=True)
