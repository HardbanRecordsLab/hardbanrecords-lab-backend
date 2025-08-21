# common/database.py - POPRAWIONA WERSJA
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str  # REQUIRED - brak wartości domyślnej
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    groq_api_key: str = "gsk_default"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Inicjalizacja settings z obsługą błędów
try:
    settings = Settings()
    print(f"✅ Settings loaded successfully")
    print(f"🗄️  Database URL configured: {settings.database_url[:20]}...")
except Exception as e:
    print(f"❌ Settings loading failed: {e}")
    print("📋 Available environment variables:")
    for key in os.environ:
        if key.upper().startswith(('DATABASE', 'SECRET', 'GROQ')):
            print(f"   {key}: {os.environ[key][:20]}...")
    raise

# Tworzenie engine z dodatkową diagnostyką
try:
    engine = create_engine(settings.database_url)
    print("✅ Database engine created successfully")
except Exception as e:
    print(f"❌ Database engine creation failed: {e}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()