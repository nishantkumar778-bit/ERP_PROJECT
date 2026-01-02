from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    age: int
    salary: int
    department: str

class Login(BaseModel):
    id: str
    password: str

class ChangePassword(BaseModel):
    new_password: str
