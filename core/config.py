from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "default"
    VERSION:str = ""
    ENVIRONMENT: str = ""
    LOG_LEVEL: str = ""
    OPENROUTER_MODEL: str = ""
    OPENROUTER_API_KEY: str = ""
    MONGODB_URI: str = ""
    MONGODB_DB_NAME: str = ""
    X_API_KEY: str = ""
    SECRET_KEY: str = ""
    ALGORITHM: str = ""
    FE_BASE_URL: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 0
    DODO_API_KEY : str = ""
    DODO_ENVIRONMENT: str = ""
    DODO_PRODUCT_ID_1: str = "pdt_0NgK79FCaFT39EWSzQDOh"
    DODO_PRODUCT_ID_2: str = "pdt_0NgK79FCaFT39EWSzQDOh"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()