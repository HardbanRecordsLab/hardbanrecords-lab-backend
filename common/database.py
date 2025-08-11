from common.database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Klasa do zarządzania zmiennymi środowiskowymi.
    Pobiera adres URL bazy danych z pliku .env na serwerze Render.
    """
    sqlalchemy_database_url: str = "postgresql://user:password@postgresserver/db"

    class Config:
        # Nazwa pliku, w którym Render przechowuje nasze sekrety
        env_file = ".env"

# Tworzymy instancję naszych ustawień
settings = Settings()

# Tworzymy "silnik" bazy danych, używając adresu URL z naszej konfiguracji
engine = create_engine(settings.sqlalchemy_database_url)

# Tworzymy "fabrykę" sesji, która będzie tworzyć połączenia z bazą
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tworzymy klasę bazową dla naszych modeli danych
# Każdy model, który stworzymy (np. User), będzie dziedziczył z tej klasy
Base = declarative_base()
Base = Base  # eksportuj Base, by był widoczny jako atrybut modułu