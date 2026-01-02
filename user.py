from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import ChangePassword
from auth import hash_password
from jwt_token import decode_token

router = APIRouter(prefix="/student")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str):
    return decode_token(token)

@router.get("/me")
def my_details(token: str, db: Session = Depends(get_db)):
    data = get_current_user(token)
    return db.query(User).filter(User.id == data["id"]).first()

@router.put("/change-password")
def change_password(data: ChangePassword, token: str, db: Session = Depends(get_db)):
    user_data = get_current_user(token)
    user = db.query(User).filter(User.id == user_data["id"]).first()
    user.password = hash_password(data.new_password)
    db.commit()
    return {"msg": "Password Updated"}
