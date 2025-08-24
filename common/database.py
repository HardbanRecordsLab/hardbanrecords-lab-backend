# common/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Wczytujemy zmienne środowiskowe z pliku .env
load_dotenv()

# Pobieramy URL bazy danych ze zmiennych środowiskowych
# Upewnij się, że masz plik .env w głównym folderze backendu
# z wpisem: DATABASE_URL="postgresql://user:password@host:port/dbname"
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("Nie zdefiniowano zmiennej środowiskowej DATABASE_URL")

# Tworzymy silnik SQLAlchemy - główny punkt połączenia z bazą danych.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Tworzymy klasę SessionLocal, która będzie fabryką sesji bazodanowych.
# Każda instancja SessionLocal będzie osobną sesją.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tworzymy bazową klasę dla naszych modeli deklaratywnych.
# Wszystkie nasze modele w bazie danych będą dziedziczyć z tej klasy.
Base = declarative_base()

# Funkcja zależności (dependency) dla FastAPI.
# Ta funkcja będzie wywoływana dla każdego żądania API, które jej wymaga.
# Otwiera nową sesję, udostępnia ją, a następnie zamyka po zakończeniu żądania.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()