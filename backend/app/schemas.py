from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class SourceOut(BaseModel):
    document_id: int
    title: str
    category: str
    source_url: str | None
    snippet: str
    score: float

class ChatRequest(BaseModel):
    question: str = Field(min_length=2, max_length=2000)

class ChatOut(BaseModel):
    id: int
    title: str
    question: str
    answer: str
    favorite: bool
    created_at: datetime
    sources: list[SourceOut] = []
    model_config = ConfigDict(from_attributes=True)

class DocumentCreate(BaseModel):
    title: str
    category: str = "General"
    source_url: str | None = None
    content: str

class DocumentOut(BaseModel):
    id: int
    title: str
    category: str
    source_url: str | None
    content: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
