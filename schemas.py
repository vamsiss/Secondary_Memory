from pydantic import BaseModel


class ChatCreate(BaseModel):
    title: str
    body: str


class ChatOut(BaseModel):
    id: int
    title: str
    body: str
