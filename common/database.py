# common/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Klasa do wczytywania wszystkich zmiennych środowiskowych z pliku .env.
    """
    # Pole do połączenia z bazą danych
    sqlalchemy_database_url: str
    
    # DODAJEMY TE TRZY POLA, aby aplikacja wiedziała, czego szukać w .env
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # Ta linijka mówi Pydantic, żeby wczytał dane z pliku .env
    model_config = SettingsConfigDict(env_file=".env")

# Tworzymy jedną, globalną instancję naszych ustawień
settings = Settings()

# Używamy wczytanych ustawień do stworzenia silnika bazy danych
engine = create_engine(settings.sqlalchemy_database_url)

# Reszta pliku bez zmian
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
