from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CommentCreate(BaseModel):
    content: str


class CommentUpdate(BaseModel):
    content: str


class CommentRead(BaseModel):
    id: int
    task_id: int
    author_id: int
    content: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
