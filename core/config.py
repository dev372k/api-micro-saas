from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "default"
    VERSION:str = ""
    ENVIRONMENT: str = ""
    LOG_LEVEL: str = ""
    MONGODB_URI: str = ""
    MONGODB_DB_NAME: str = ""
    X_API_KEY: str = ""
    DODO_API_KEY : str = ""
    DODO_PRODUCT_ID_1: str = "pdt_0NgK79FCaFT39EWSzQDOh"
    DODO_PRODUCT_ID_2: str = "pdt_0NgK79FCaFT39EWSzQDOh"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()