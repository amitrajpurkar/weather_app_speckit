"""DTOs for monthly trend endpoint."""

from typing import List, Optional

from pydantic import BaseModel, Field


class DailyAggregateDto(BaseModel):
    day: int = Field(..., ge=1, le=31, description="Day of month (1–31)")
    avg_temperature: Optional[float] = Field(None, description="Average temperature for the day")
    avg_humidity: Optional[float] = Field(None, description="Average humidity for the day")
    observation_count: int = Field(..., ge=0, description="Number of observations used")


class MonthlyTrendResponse(BaseModel):
    year: int = Field(..., description="Year for the trend (same as yearly summary year)")
    month: int = Field(..., ge=1, le=12, description="Month number (1–12)")
    daily_aggregates: List[DailyAggregateDto] = Field(..., description="Daily aggregates for the month")
    most_common_condition: Optional[str] = Field(None, description="Most frequent weather condition in the month")
