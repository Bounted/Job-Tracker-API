from typing import Annotated
from fastapi import Depends, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from schemas.auth import Token, RefreshRequest
from core.exceptions import AuthenticationError
from services.auth_service import login, refresh_access_token, logout_service
from api.deps import get_current_user
from models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token", status_code=status.HTTP_200_OK)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db),
) -> Token:
    tokens = await login(db, form_data.username, form_data.password)
    if not tokens:
        raise AuthenticationError("Неверное имя пользователя или пароль.")
    access_token, refresh_token = tokens
    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
    responses={401: {"description": "Refresh токен недействителен или истёк"}},
)
async def refresh_token(
    body: RefreshRequest, db: AsyncSession = Depends(get_db)
) -> Token:
    access, refresh = await refresh_access_token(db, body.refresh_token)
    return Token(access_token=access, refresh_token=refresh)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    await logout_service(db, current_user.id)  # type: ignore
