# auth_app/main.py

# Krok 1: Importujemy wszystkie potrzebne narzędzia
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Krok 2: Importujemy nasze własne moduły
# 'models' i 'database' bierzemy ze współdzielonego folderu 'common'
from common import models
from common.database import SessionLocal, engine
# 'crud' i 'schemas' bierzemy z bieżącego folderu 'auth_app'
from . import crud, schemas

# Krok 3: Komenda tworząca tabele w bazie danych.
# Musi być wykonana po zaimportowaniu modeli i silnika bazy.
models.Base.metadata.create_all(bind=engine)

# Krok 4: Inicjalizacja aplikacji i routera
app = FastAPI()
router = APIRouter()

# Krok 5: Funkcja pomocnicza do zarządzania sesjami bazy danych
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Krok 6: Definicja endpointu do rejestracji
@router.post("/register", response_model=schemas.UserOut, tags=["Authentication"])
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Rejestruje nowego użytkownika w systemie.
    Sprawdza, czy email nie jest już zajęty.
    Haszuje hasło przed zapisem do bazy.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    created_user = crud.create_user(db=db, user=user)
    return created_user

# Krok 7: Definicja głównego endpointu do sprawdzania, czy serwis działa
@router.get("/", tags=["Status"])
def read_root():
    """
    Zwraca informację, że serwis jest uruchomiony.
    """
    return {"message": "Auth Service is running!"}

# Krok 8: Podłączenie naszego routera do głównej aplikacji
app.include_router(router)