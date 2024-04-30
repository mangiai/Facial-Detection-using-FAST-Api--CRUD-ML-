from sqlalchemy.orm import Session
from .models import User
from fastapi import HTTPException, status

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user_name: str):
    db_user = User(name=user_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_name(db: Session, user_id: int, name: str):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        return None
    db_user.name = name
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    db.delete(user)
    db.commit()
