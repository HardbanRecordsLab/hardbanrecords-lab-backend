# auth_app/main.py

# Krok 1: Importujemy wszystkie potrzebne narzędzia z bibliotek zewnętrznych
from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

# Krok 2: Importujemy nasze własne moduły
# 'models' importujemy, aby SQLAlchemy wiedziało o istnieniu naszej tabeli User
from common import models
# 'engine', 'SessionLocal', 'Base' i 'settings' bierzemy z naszego pliku database.py
from common.database import SessionLocal, engine, Base, settings
# 'crud' i 'schemas' bierzemy z bieżącego folderu 'auth_app'
from . import crud, schemas

# Krok 3: Komenda tworząca tabele w bazie danych.
# Używamy obiektu 'Base' bezpośrednio z pliku database.py, w którym został zdefiniowany.
Base.metadata.create_all(bind=engine)

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
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    created_user = crud.create_user(db=db, user=user)
    return created_user

# Krok 7: Definicja endpointu do logowania
@router.post("/login", response_model=schemas.Token, tags=["Authentication"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Loguje użytkownika i zwraca token dostępowy JWT.
    """
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not crud.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = crud.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Krok 8: Definicja głównego endpointu do sprawdzania, czy serwis działa
@router.get("/", tags=["Status"])
def read_root():
    """
    Zwraca informację, że serwis jest uruchomiony.
    """
    return {"message": "Auth Service is running!"}

# Krok 9: Podłączenie naszego routera do głównej aplikacji
app.include_router(router)
