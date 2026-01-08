from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    age: int
    salary: float
    department: str

class UserUpdate(BaseModel):
    name: Optional[str]
    age: Optional[int]
    salary: Optional[float]
    department: Optional[str]

class UserOut(BaseModel):
    id: str
    name: str
    age: int
    salary: float
    department: str
    present: bool

    class Config:
        orm_mode = True

class LeaveOut(BaseModel):
    id: int
    status: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class NotificationOut(BaseModel):
    id: int
    message: str
    is_read: bool

    class Config:
        orm_mode = True
