from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = ""
    VERSION:str = ""
    ENVIRONMENT: str = ""
    LOG_LEVEL: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()