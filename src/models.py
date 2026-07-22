from pydantic import BaseModel, HttpUrl
from typing import List
from enum import Enum


class Source(BaseModel):
    title: str
    url: HttpUrl

class ConfidenceLevel(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    
class ResearchResponse(BaseModel):
    summary: str
    key_points: List[str]
    analysis: str
    sources: List[Source]
    confidence: ConfidenceLevel

