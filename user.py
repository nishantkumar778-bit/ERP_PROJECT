from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import ChangePassword
from auth import hash_password, verify_password
from jwt_token import decode_token

router = APIRouter(prefix="/student")

# database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# get logged-in student from token
def get_current_user(token: str):
    return decode_token(token)

# ✅ Student can see all details
@router.get("/me")
def view_my_details(token: str, db: Session = Depends(get_db)):
    user_data = get_current_user(token)
    student = db.query(User).filter(User.id == user_data["id"]).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return {
        "student_id": student.id,
        "name": student.name,
        "age": student.age,
        "department": student.department,
        "salary": student.salary,
        "attendance": "Present" if student.present else "Absent"
    }

# ✅ Student can change password (requires current password)
@router.put("/change-password")
def change_password(data: ChangePassword, token: str, db: Session = Depends(get_db)):
    user_data = get_current_user(token)
    student = db.query(User).filter(User.id == user_data["id"]).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Verify current password
    if not verify_password(data.current_password, student.password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    # Update to new password
    student.password = hash_password(data.new_password)
    db.commit()

    return {"message": "Password updated successfully"}
