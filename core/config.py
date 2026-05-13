from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str 
    TESTING: bool = False


    model_config = SettingsConfigDict(
#        env_file=".env",
        env_file=".env.test" if Path(".env.test").exists() and not Path(".env").exists() else ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings() # type: ignore