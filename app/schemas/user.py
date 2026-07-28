from pydantic import BaseModel, EmailStr
from typing import Optional
from app.schemas.project import ProjectRead
from app.schemas.task import TaskRead


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserProfileRead(UserRead):
    projects: list[ProjectRead] = []
    tasks: list[TaskRead] = []
