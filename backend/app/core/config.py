from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # App Info
    APP_NAME: str = "Backend"
    APP_VERSION: str = "1.0.0"

    # CORS
    FRONTEND_URLS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # ...

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
    }

settings = Settings()
