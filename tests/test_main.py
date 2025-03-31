import pytest
import pandas as pd
from main import get_pitch_summary

@pytest.mark.asyncio
async def test_get_pitch_summary_success(monkeypatch):
    # Mock statcast to return a sample DataFrame (synchronous)
    def mock_statcast(start_dt, end_dt):
        data = pd.DataFrame({
            "release_speed": [90.0, 95.0, 100.0]
        })
        return data
    
    monkeypatch.setattr("main.statcast", mock_statcast)
    result = await get_pitch_summary("2023-06-01")
    assert result == {
        "date": "2023-06-01",
        "average_pitch_speed": 95.0,
        "max_pitch_speed": 100.0,
        "total_pitches": 3
    }

@pytest.mark.asyncio
async def test_get_pitch_summary_empty_data(monkeypatch):
    # Mock statcast to return an empty DataFrame (synchronous)
    def mock_statcast(start_dt, end_dt):
        return pd.DataFrame()
    
    monkeypatch.setattr("main.statcast", mock_statcast)
    result = await get_pitch_summary("2023-06-01")
    assert result == {"error": "No data available for this date"}

@pytest.mark.asyncio
async def test_get_pitch_summary_exception(monkeypatch):
    # Mock statcast to raise an exception (synchronous)
    def mock_statcast(start_dt, end_dt):
        raise ValueError("API error")
    
    monkeypatch.setattr("main.statcast", mock_statcast)
    result = await get_pitch_summary("2023-06-01")
    assert "error" in result
    assert result["error"] == "Unexpected error: API error"

@pytest.mark.asyncio
async def test_get_pitch_summary_invalid_date(monkeypatch):
    # Mock statcast to simulate invalid date handling (synchronous)
    def mock_statcast(start_dt, end_dt):
        return pd.DataFrame()  # Empty for invalid date
    
    monkeypatch.setattr("main.statcast", mock_statcast)
    result = await get_pitch_summary("invalid-date")
    assert result == {"error": "No data available for this date"}
