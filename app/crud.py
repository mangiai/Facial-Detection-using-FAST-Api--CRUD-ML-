from sqlalchemy.orm import Session
from .models import User

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user_name: str):
    db_user = User(name=user_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, new_name: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.name = new_name
        db.commit()
        return user
    return None
