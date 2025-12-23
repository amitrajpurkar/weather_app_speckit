"""Integration tests for /api/v1/monthly-trend endpoint."""

from pathlib import Path

from fastapi.testclient import TestClient

from src.infrastructure.csv_loader import load_weather_data
from src.main import app


client = TestClient(app)


def test_monthly_trend_success(sample_csv_path: Path, monkeypatch):
    def mock_load_weather_data(path: Path):
        return load_weather_data(sample_csv_path)

    monkeypatch.setattr("src.api.v1.monthly_trend.load_weather_data", mock_load_weather_data)

    response = client.get("/api/v1/monthly-trend", params={"month": 1})
    assert response.status_code == 200
    payload = response.json()

    assert payload["year"] == 2024
    assert payload["month"] == 1
    assert payload["most_common_condition"] == "clear"

    # Only days that exist in sample_csv_path (day 1 and day 2) should be present
    days = [d["day"] for d in payload["daily_aggregates"]]
    assert days == [1, 2]


def test_monthly_trend_no_data_for_month_returns_404(sample_csv_path: Path, monkeypatch):
    def mock_load_weather_data(path: Path):
        return load_weather_data(sample_csv_path)

    monkeypatch.setattr("src.api.v1.monthly_trend.load_weather_data", mock_load_weather_data)

    response = client.get("/api/v1/monthly-trend", params={"month": 12})
    assert response.status_code == 404
