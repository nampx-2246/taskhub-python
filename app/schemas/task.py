from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "todo"
    priority: Optional[str] = "medium"
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    project_id: int
    assignee_id: Optional[int] = None


class TaskRead(TaskBase):
    id: int
    project_id: int
    assignee_id: Optional[int] = None

    class Config:
        from_attributes = True
