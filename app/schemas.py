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
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True) 