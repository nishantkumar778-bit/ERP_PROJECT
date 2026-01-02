from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import UserCreate
from auth import hash_password

router = APIRouter(prefix="/admin")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_id(db, name):
    count = db.query(User).filter(User.name == name).count()
    return name + str(count + 1).zfill(3)

@router.post("/create")
def create_student(data: UserCreate, db: Session = Depends(get_db)):
    student_id = generate_id(db, data.name)

    user = User(
        id=student_id,
        name=data.name,
        age=data.age,
        salary=data.salary,
        department=data.department,
        password=hash_password("123456"),
        role="student"
    )

    db.add(user)
    db.commit()
    return {"id": student_id}

@router.get("/all")
def all_students(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/search")
def search(q: str, db: Session = Depends(get_db)):
    return db.query(User).filter(
        (User.id.contains(q)) | (User.name.contains(q))
    ).all()

@router.put("/attendance/{id}")
def mark_attendance(id: str, present: bool, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    user.present = present
    db.commit()
    return {"msg": "Attendance Updated"}

@router.delete("/delete/{id}")
def delete_student(id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    db.delete(user)
    db.commit()
    return {"msg": "Deleted"}
