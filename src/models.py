from enum import Enum

from pydantic import BaseModel, HttpUrl


class Source(BaseModel):
    title: str
    url: HttpUrl | None = None


class ConfidenceLevel(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class ResearchResponse(BaseModel):
    summary: str
    key_points: list[str]
    analysis: str
    confidence: ConfidenceLevel


class QueryPlannerResponse(BaseModel):
    queries: list[str]