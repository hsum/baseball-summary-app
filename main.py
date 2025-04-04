from typing import Dict, Any
from fastapi import FastAPI, Request
import functions_framework
import pandas as pd
from pybaseball import statcast
import click
import asyncio
import json

app = FastAPI(title="Baseball Pitch Summary")

@app.get("/pitch-summary/{date}", response_model=Dict[str, Any])
async def get_pitch_summary(date: str) -> Dict[str, Any]:
    """Fetch and summarize pitch speeds for a given date."""
    try:
        data: pd.DataFrame = statcast(start_dt=date, end_dt=date)
        if data.empty:
            return {"error": "No data available for this date"}
        
        avg_speed: float = data["release_speed"].mean()
        max_speed: float = data["release_speed"].max()
        pitch_count: int = len(data)
        
        if pd.isna(avg_speed) or pd.isna(max_speed):
            return {"error": "Invalid pitch data returned"}
        
        return {
            "date": date,
            "average_pitch_speed": float(avg_speed),
            "max_pitch_speed": float(max_speed),
            "total_pitches": int(pitch_count)
        }
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

@functions_framework.http
def gcp_pitch_summary(request):
    """Entry point for GCP Cloud Functions."""
    path = request.path.strip('/')  # Remove leading/trailing slashes
    if not path:  # Handle empty path
        return json.dumps({"error": "No date provided"})
    date = path  # Treat path as date
    result = asyncio.run(get_pitch_summary(date))  # Run async function synchronously
    return json.dumps(result)

@click.command()
@click.option("--date", required=True, type=str, help="Date in YYYY-MM-DD format")
def cli(date: str) -> None:
    """CLI to fetch pitch summary locally."""
    result: Dict[str, Any] = asyncio.run(get_pitch_summary(date))
    click.echo(result)

if __name__ == "__main__":
    cli()
