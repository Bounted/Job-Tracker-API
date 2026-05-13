from sqlalchemy.orm import Session
from datetime import timedelta
from core.security import verify_password, create_access_token, DUMMY_HASH
from services.user_service import get_user_by_name_or_none
from core.config import settings

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_name_or_none(db, username) 
    if not user:
        verify_password(password, DUMMY_HASH)  
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def login(db: Session, username: str, password: str):
    user = authenticate_user(db, username, password)
    if not user:
        return None
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_access_token(
        data={"sub": user.name},
        expires_delta=access_token_expires,
    )

