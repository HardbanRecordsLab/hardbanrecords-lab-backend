# common/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Pole, które już mieliśmy
    sqlalchemy_database_url: str
    
    # Dodajemy pola, których oczekujemy z pliku .env
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # Ta linijka mówi Pydantic, żeby wczytał dane z pliku .env
    model_config = SettingsConfigDict(env_file=".env")

# Tworzymy instancję naszych ustawień
settings = Settings()

# Reszta pliku bez zmian
engine = create_engine(settings.sqlalchemy_database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()