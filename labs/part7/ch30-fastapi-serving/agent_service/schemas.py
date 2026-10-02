from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500, examples=["휴관일을 알려 주세요"])
    thread_id: str = Field(pattern=r"^[a-zA-Z0-9_-]{1,64}$", examples=["demo-01"])


class ChatResponse(BaseModel):
    answer: str
    thread_id: str


class HealthResponse(BaseModel):
    status: str
