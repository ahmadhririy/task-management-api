from pydantic import BaseModel, EmailStr, Field
from typing import Literal

### user ###
class UserCreate(BaseModel):
    name:str =Field(min_length=3,max_length=30)
    email:EmailStr
    password:str = Field(min_length=8)


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr


class UserLogin(BaseModel):
    email:EmailStr
    password:str 


### project ###

class ProjectCreate(BaseModel):
    name: str = Field(min_length=3 , max_length= 30)
    description: str | None = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    user_id: int


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = None


### tasks ###


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    project_id: int


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    description: str | None = None
    status: Literal["todo", "in_progress", "done"] = "todo"


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=150)
    description: str | None = None
    status: Literal["todo", "in_progress", "done"] | None = None