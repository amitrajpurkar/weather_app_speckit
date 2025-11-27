"""DTOs for yearly summary endpoint."""

from typing import List, Optional

from pydantic import BaseModel, Field


class MonthlySummaryDto(BaseModel):
    month: int = Field(..., ge=1, le=12, description="Month number (1–12)")
    avg_temperature: Optional[float] = Field(None, description="Average temperature for the month")
    avg_humidity: Optional[float] = Field(None, description="Average humidity for the month")
    observation_count: int = Field(..., ge=0, description="Number of observations used")


class YearlySummaryResponse(BaseModel):
    year: Optional[int] = Field(None, description="Year used for the summary (latest full year)")
    months: List[MonthlySummaryDto] = Field(..., description="Monthly summaries for the year")
