from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import UserCreate, UserUpdate
from auth import hash_password

router = APIRouter(prefix="/admin")

# Database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Auto-generate student ID
def generate_id(db, name):
    count = db.query(User).filter(User.name == name).count()
    return name + str(count + 1).zfill(3)

# Create student
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

# Get all students
@router.get("/all")
def all_students(db: Session = Depends(get_db)):
    return db.query(User).all()

# Search student
@router.get("/search")
def search(q: str, db: Session = Depends(get_db)):
    return db.query(User).filter(
        (User.id.contains(q)) | (User.name.contains(q))
    ).all()

# Mark attendance
@router.put("/attendance/{id}")
def mark_attendance(id: str, present: bool, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.present = present
    db.commit()
    return {"msg": "Attendance Updated"}

# Delete student
@router.delete("/delete/{id}")
def delete_student(id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"msg": "Deleted"}

# ✅ Flexible Update student details
@router.put("/update/{id}")
def update_student(id: str, data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update only fields provided
    if data.name is not None:
        user.name = data.name
    if data.age is not None:
        user.age = data.age
    if data.salary is not None:
        user.salary = data.salary
    if data.department is not None:
        user.department = data.department

    db.commit()
    return {"msg": "Student details updated"}
