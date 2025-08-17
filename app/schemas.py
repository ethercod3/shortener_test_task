from pydantic import BaseModel, Field
from datetime import datetime

class ShortenRequest(BaseModel):
    url: str = Field(..., description="Оригинальный URL для сокращения")

class ShortenResponse(BaseModel):
    code: str
    short_url: str

class StatsResponse(BaseModel):
    code: str
    url: str
    clicks: int
    created_at: datetime