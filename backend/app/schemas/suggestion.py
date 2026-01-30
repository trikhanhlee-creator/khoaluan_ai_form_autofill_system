from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class SuggestionBase(BaseModel):
    value: str
    frequency: int
    ranking: int


class SuggestionResponse(SuggestionBase):
    pass


class SuggestionsListResponse(BaseModel):
    user_id: int
    field_id: int
    suggestions: List[SuggestionResponse]
    total_count: int
    message: str = "Suggestions retrieved successfully"


class SuggestionsErrorResponse(BaseModel):
    error: str
    message: str
    status_code: int


class FieldStatisticsResponse(BaseModel):
    total_entries: int
    recent_entries_count: int
    unique_values: int
    frequency_distribution: dict
