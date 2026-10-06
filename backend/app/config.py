import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "mysql+pymysql://coderag:coderag_password@localhost:3306/coderag")
    cors_origins: str = os.getenv("CORS_ORIGINS", "http://localhost:5173")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

settings = Settings()
