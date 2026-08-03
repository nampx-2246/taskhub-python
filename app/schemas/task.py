from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.tag import TagRead


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "todo"
    priority: Optional[str] = "medium"
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    project_id: int
    assignee_id: Optional[int] = None
    tag_ids: Optional[list[int]] = []


class TaskCreateInProject(TaskBase):
    assignee_id: Optional[int] = None
    tag_ids: Optional[list[int]] = []


class TaskAssign(BaseModel):
    assignee_id: int


class TaskRead(TaskBase):
    id: int
    project_id: int
    assignee_id: Optional[int] = None
    created_at: Optional[datetime] = None
    tags: list[TagRead] = []

    class Config:
        from_attributes = True
