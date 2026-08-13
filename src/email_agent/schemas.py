from typing import Literal

from pydantic import BaseModel, Field


class Email(BaseModel):
    id: str
    sender: str
    subject: str
    body: str
    timestamp: str

class TriageResult(BaseModel):
    action: Literal["respond", "notify", "ignore"]
    reason: str = Field(description="Brief justification for the triage decision")