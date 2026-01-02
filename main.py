from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import User
from schemas import Login
from auth import verify_password
from jwt_token import create_token
import admin, user

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(admin.router)
app.include_router(user.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/login")
def login(data: Login, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == data.id).first()
    if not user or not verify_password(data.password, user.password):
        return {"error": "Invalid login"}

    token = create_token({"id": user.id})
    return {"token": token}
