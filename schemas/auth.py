from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = Field(default="bearer", description="Тип токена")


class TokenData(BaseModel):
    username: str


class RefreshRequest(BaseModel):
    refresh_token: str

    