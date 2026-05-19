from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "default"
    VERSION:str = ""
    ENVIRONMENT: str = ""
    LOG_LEVEL: str = ""
    OPENROUTER_MODEL: str = ""
    OPENROUTER_API_KEY: str = ""
    RAPIDAPI_PROXY_SECRET_KEY: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()