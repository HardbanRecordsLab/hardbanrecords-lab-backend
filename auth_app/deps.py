from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from common import models
from common.database import get_db
from auth_app import schemas
import os

# Schemat OAuth2, który wskazuje, skąd pobrać token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> models.User:
    """
    Dekoduje token JWT, weryfikuje go i zwraca obiekt użytkownika z bazy danych.
    To jest główna funkcja zabezpieczająca endpointy.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except (JWTError, ValidationError):
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_user_id(current_user: models.User = Depends(get_current_user)) -> int:
    """
    Zależność, która pobiera pełny obiekt użytkownika, ale zwraca tylko jego ID.
    Jest to wygodne w endpointach, gdzie potrzebujemy tylko ID właściciela.
    """
    return current_user.id