from sqlalchemy.orm import Session
import models, auth


def generate_user_id(db: Session, name: str):
    count = db.query(models.User).filter(models.User.name == name).count() + 1
    return f"{name}{str(count).zfill(3)}"


def create_user(db: Session, name: str, age: int, salary: float, department: str, is_admin=False):
    user_id = generate_user_id(db, name)
    hashed_password = auth.hash_password("123456")
    user = models.User(
        id=user_id,
        name=name,
        age=age,
        salary=salary,
        department=department,
        password=hashed_password,
        is_admin=is_admin
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def update_user(db: Session, user: models.User, data: dict):
    for key, value in data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: models.User):
    db.delete(user)
    db.commit()


def mark_attendance(db: Session, user: models.User, present: bool):
    user.present = present
    db.commit()
    db.refresh(user)
    return user


def apply_leave(db: Session, user: models.User):
    leave = models.Leave(user_id=user.id)
    db.add(leave)
    db.commit()
    db.refresh(leave)
    return leave


# 🔔 Notification Logic
def create_notification(db: Session, user_id: str, message: str):
    notification = models.Notification(
        user_id=user_id,
        message=message
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


def approve_leave(db: Session, leave: models.Leave):
    leave.status = "approved"
    db.commit()
    db.refresh(leave)

    create_notification(
        db,
        leave.user_id,
        "Your leave has been APPROVED"
    )
    return leave


def reject_leave(db: Session, leave: models.Leave):
    leave.status = "rejected"
    db.commit()
    db.refresh(leave)

    create_notification(
        db,
        leave.user_id,
        "Your leave has been REJECTED"
    )
    return leave
