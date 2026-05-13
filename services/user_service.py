from sqlalchemy.orm import Session
from core.security import password_hash
from repositories.user_repo import get_by_id, get_by_name, create, delete
from schemas.user import UserCreate
from core.exceptions import NotFoundError, AlreadyExistsError
from sqlalchemy.exc import IntegrityError


def ensure_user_exists(db: Session, name: str):
    user = get_by_name(db, name)
    if user is None:
        raise NotFoundError("A user with this name does not exist.")
    return user


def get_user_by_name_or_none(db: Session, name: str):
    return get_by_name(db, name)


def get_user_by_id(db: Session, user_id: int):
    user = get_by_id(db, user_id)
    if user is None:
        raise NotFoundError("A user with this ID does not exist.")
    return user


def delete_user(db: Session, user_id: int):
    get_user_by_id(db, user_id)
    delete(db, user_id)


def create_user(db: Session, user: UserCreate):
    hashed = password_hash.hash(user.password)
    try:
        return create(db, user.name, hashed)
    except IntegrityError:
        raise AlreadyExistsError("A user with this name already exists.")
