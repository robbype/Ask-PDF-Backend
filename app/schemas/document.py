from pydantic import BaseModel
from datetime import datetime


class DocumentRequest(BaseModel):
    name: str
    file_path: str


class DocumentResponse(BaseModel):
    id: int
    name: str
    file_path: str
    created_at: datetime

    class Config:
        orm_mode = True
