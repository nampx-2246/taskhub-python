from typing import Optional
from pydantic import BaseModel, EmailStr
from app.schemas.project import ProjectRead
from app.schemas.task import TaskRead


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    is_active: Optional[bool] = True


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    password: str


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserRead(UserBase):
    id: int
    role: str = "user"

    class Config:
        from_attributes = True


class UserProfileRead(UserRead):
    projects: list[ProjectRead] = []
    tasks: list[TaskRead] = []


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None
