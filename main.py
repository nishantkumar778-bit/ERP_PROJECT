from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
import database, models, schemas, crud, auth, dependencies

app = FastAPI(title="Student Management System")

# ---- Login ----
@app.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_access_token({"sub": user.id})
    return {"access_token": token, "token_type": "bearer"}

# ---- Admin Routes ----
@app.post("/admin/create_user", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db), _: models.User = Depends(dependencies.admin_required)):
    return crud.create_user(db, user.name, user.age, user.salary, user.department)

@app.get("/admin/users", response_model=List[schemas.UserOut])
def get_all_users(db: Session = Depends(database.get_db), _: models.User = Depends(dependencies.admin_required)):
    return crud.get_users(db)

@app.put("/admin/user/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: str, user: schemas.UserUpdate, db: Session = Depends(database.get_db), _: models.User = Depends(dependencies.admin_required)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db, db_user, user.dict(exclude_unset=True))

@app.delete("/admin/user/{user_id}")
def delete_user(user_id: str, db: Session = Depends(database.get_db), _: models.User = Depends(dependencies.admin_required)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, db_user)
    return {"detail": "User deleted"}

@app.put("/admin/attendance/{user_id}")
def mark_attendance(user_id: str, present: bool, db: Session = Depends(database.get_db), _: models.User = Depends(dependencies.admin_required)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.mark_attendance(db, user, present)

@app.put("/admin/leave/{leave_id}/approve")
def approve_leave(leave_id: int, db: Session = Depends(database.get_db), _: models.User = Depends(dependencies.admin_required)):
    leave = db.query(models.Leave).filter(models.Leave.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    return crud.approve_leave(db, leave)

@app.put("/admin/leave/{leave_id}/reject")
def reject_leave(leave_id: int, db: Session = Depends(database.get_db), _: models.User = Depends(dependencies.admin_required)):
    leave = db.query(models.Leave).filter(models.Leave.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    return crud.reject_leave(db, leave)

# ---- New: Search users by ID or name ----
@app.get("/admin/search_users", response_model=List[schemas.UserOut])
def search_users(query: str, db: Session = Depends(database.get_db), _: models.User = Depends(dependencies.admin_required)):
    users = db.query(models.User).filter(
        (models.User.id.like(f"%{query}%")) | 
        (models.User.name.like(f"%{query}%"))
    ).all()
    return users

# ---- New: Show leaves of a user ----
@app.get("/admin/user/{user_id}/leaves", response_model=List[schemas.LeaveOut])
def get_user_leaves(user_id: str, db: Session = Depends(database.get_db), _: models.User = Depends(dependencies.admin_required)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.leaves

# ---- User Routes ----
@app.get("/user/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(dependencies.get_current_user)):
    return current_user

@app.put("/user/change_password")
def change_password(new_password: str, current_user: models.User = Depends(dependencies.get_current_user), db: Session = Depends(database.get_db)):
    current_user.password = auth.hash_password(new_password)
    db.commit()
    return {"detail": "Password changed successfully"}

@app.post("/user/apply_leave", response_model=schemas.LeaveOut)
def user_apply_leave(current_user: models.User = Depends(dependencies.get_current_user), db: Session = Depends(database.get_db)):
    return crud.apply_leave(db, current_user)
