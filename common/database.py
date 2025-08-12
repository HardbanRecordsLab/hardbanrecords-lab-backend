# common/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic_settings import BaseSettings, SettingsConfigDict # Dodajemy SettingsConfigDict

class Settings(BaseSettings):
    """
    Klasa do zarządzania zmiennymi środowiskowymi.
    """
    sqlalchemy_database_url: str 

    # Ta nowa sekcja mówi Pydantic, żeby szukał pliku .env
    model_config = SettingsConfigDict(env_file=".env")

# Tworzymy instancję naszych ustawień
settings = Settings()

# Tworzymy "silnik" bazy danych, używając adresu URL z naszej konfiguracji
engine = create_engine(settings.sqlalchemy_database_url)

# Tworzymy "fabrykę" sesji
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tworzymy klasę bazową dla naszych modeli
Base = declarative_base()