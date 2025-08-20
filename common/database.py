# common/database.py - Zaktualizowany
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # ZMIANA: Usunięto domyślną wartość. Aplikacja nie uruchomi się bez tej zmiennej.
    database_url: str 
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    groq_api_key: str = "gsk_default"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

# ZMIANA: Uproszczono logikę tworzenia silnika bazy danych
engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ZMIANA: Centralna funkcja do pobierania sesji DB, aby uniknąć powtórzeń
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
