# File: schemas.py
from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    age: int
    salary: int
    department: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    salary: Optional[int] = None
    department: Optional[str] = None

# ✅ For student changing password
class ChangePassword(BaseModel):
    current_password: str  # current password for verification
    new_password: str      # new password to update
