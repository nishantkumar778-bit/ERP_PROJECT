from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)   # UUID or custom ID
    name = Column(String(100), nullable=False)
    age = Column(Integer)
    salary = Column(Float)
    department = Column(String(50))
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    present = Column(Boolean, default=False)

    leaves = relationship("Leave", back_populates="user")


class Leave(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"))
    status = Column(String(20), default="pending")

    user = relationship("User", back_populates="leaves")
