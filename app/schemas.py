from datetime import datetime

from pydantic import BaseModel, ConfigDict

class CreateNote(BaseModel):
    title: str
    content: str

class UpdateNote(BaseModel):
    title: str | None = None
    content: str | None = None

class ResponseNote(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True) 