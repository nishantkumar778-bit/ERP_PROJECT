from sqlalchemy import Column, String, Integer, Boolean
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String(50), primary_key=True)
    name = Column(String(100))
    age = Column(Integer)
    salary = Column(Integer)
    department = Column(String(100))
    password = Column(String(200))
    present = Column(Boolean, default=False)
    role = Column(String(20))   # admin / student
