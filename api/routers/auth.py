from typing import Annotated
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from schemas.auth import Token
from core.exceptions import authentication_exception
from services.auth_service import login

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db),
) -> Token:
    access_token = await login(db, form_data.username, form_data.password)
    if not access_token:
        raise authentication_exception
    return Token(access_token=access_token, token_type="bearer")
