from pydantic import BaseModel
from typing import Optional
from app.schemas.task import TaskRead


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    owner_id: int


class ProjectRead(ProjectBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class ProjectWithTasksRead(ProjectRead):
    tasks: list[TaskRead] = []
