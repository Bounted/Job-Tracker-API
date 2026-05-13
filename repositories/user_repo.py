from sqlalchemy.orm import Session
from models.user import User


def get_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_by_name(db: Session, name: str):
    return db.query(User).filter(User.name == name).first()


def create(db: Session, name: str, hashed_password: str):
    user = User(name=name, hashed_password=hashed_password)
    db.add(user)
    db.flush()
    return user
 

def delete(db: Session, user_id: int):
    db.query(User).filter(User.id == user_id).delete()
    db.flush()
