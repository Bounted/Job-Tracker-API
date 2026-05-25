from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserCreate, UserRead
from services.user_service import create_user, get_user_by_id, delete_user
from db.session import get_db
from api.deps import get_current_user
from models.user import User


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user_route(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user)


@router.get("/me", response_model=UserRead, status_code=status.HTTP_200_OK)
async def get_user_route(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    return await get_user_by_id(db, current_user.id)  # type: ignore


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_route(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await delete_user(db, current_user.id)  # type: ignore