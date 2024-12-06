from __future__ import annotations
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Union
from datetime import datetime

class Metric(BaseModel):
    value: str
    context: str
    verified: bool = False
    category: Optional[str]
    timeframe: Optional[str]
    impact_area: Optional[str]

class Variation(BaseModel):
    short: str
    medium: str
    detailed: str

class Dates(BaseModel):
    start: str
    end: str

    @validator('start', 'end')
    def validate_date_format(cls, v):
        if v != 'present':
            try:
                datetime.strptime(v, '%Y-%m')
            except ValueError:
                raise ValueError('Date must be in YYYY-MM format')
        return v

class Achievement(BaseModel):
    id: str
    core: str
    dates: Dates
    variations: Dict[str, Variation]
    metrics: List[Metric]
    impact: List[str]
    technical_details: Optional[List[str]]
    skills: Optional[List[str]]
    tags: Optional[List[str]]

    class Config:
        extra = "allow"
