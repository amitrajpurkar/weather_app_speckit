"""Integration tests for /api/v1/yearly-summary endpoint."""

import pytest
from fastapi.testclient import TestClient
from pathlib import Path

from src.main import app
from src.infrastructure.csv_loader import load_weather_data


client = TestClient(app)


def test_yearly_summary_success(sample_csv_path: Path, monkeypatch):
    """Endpoint returns 200 and proper structure for sample data."""
    # Monkeypatch the CSV path used by the endpoint
    def mock_load_weather_data(path: Path):
        # Ignore path argument and use our sample CSV
        return load_weather_data(sample_csv_path)

    monkeypatch.setattr("src.api.v1.yearly_summary.load_weather_data", mock_load_weather_data)

    response = client.get("/api/v1/yearly-summary")
    assert response.status_code == 200
    payload = response.json()
    assert "year" in payload
    assert "months" in payload
    assert isinstance(payload["months"], list)
    # Sample data has months 1 and 2; expect 12 entries with some nulls
    assert len(payload["months"]) == 12
    for month in payload["months"]:
        assert "month" in month
        assert "avg_temperature" in month
        assert "avg_humidity" in month
        assert "observation_count" in month


def test_yearly_summary_no_data(tmp_path: Path, monkeypatch):
    """Endpoint returns empty summaries when CSV has no matching data."""
    empty_csv = tmp_path / "WeatherData.csv"
    empty_csv.write_text("timestamp,temperature,humidity,condition\n")
    monkeypatch.setattr("src.api.v1.yearly_summary.load_weather_data", lambda p: load_weather_data(empty_csv))

    response = client.get("/api/v1/yearly-summary")
    assert response.status_code == 200
    payload = response.json()
    assert payload["year"] is None
    assert payload["months"] == []


def test_health_endpoint():
    """Health check returns 200 and ok status."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
