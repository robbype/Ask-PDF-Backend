from pydantic import BaseModel


class MessageRequest(BaseModel):
    document_id: str
    question: str
