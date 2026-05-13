from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserRead
from services.user_service import create_user, get_user_by_id, delete_user
from db.session import get_db
from api.deps import get_current_user
from models.user import User
from core.exceptions import AlreadyExistsError, NotFoundError

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return create_user(db, user)
    except AlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/me", response_model=UserRead, status_code=status.HTTP_200_OK)
def get_user_route(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    try:
        return get_user_by_id(db, current_user.id)
    except NotFoundError as n:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(n))


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_route(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        delete_user(db, current_user.id)
    except NotFoundError as n:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(n))