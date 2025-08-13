# auth_app/crud.py
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

from common import models
from common.database import settings # Importujemy nasze ustawienia
from . import schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """Weryfikuje, czy hasło w czystym tekście pasuje do zahashowanego."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Tworzy nowy token dostępowy (JWT)."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, 
        settings.secret_key, # Używamy SECRET_KEY z .env
        algorithm=settings.algorithm # Używamy ALGORITHM z .env
    )
    return encoded_jwt

def get_user_by_email(db: Session, email: str):
    """Sprawdza, czy użytkownik o danym emailu już istnieje."""
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    """Tworzy nowego użytkownika w bazie danych."""
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user