from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from schemas import UserCreate, UserRead
from crud import create_user, get_user_by_id, delete_user
from database import get_db
from auth import get_current_user
from models import User

router = APIRouter(prefix="/users")


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@router.get("/me", response_model=UserRead)
def get_user_route(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return get_user_by_id(db, current_user.id)



@router.delete("/", status_code=status.HTTP_200_OK)
def delete_user_router(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return delete_user(db, current_user.id)
