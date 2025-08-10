# auth_app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from common import models
from common.database import SessionLocal, engine
from . import crud, schemas

# Tworzy tabele w bazie danych (jeśli nie istnieją)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Funkcja do zarządzania sesjami bazy danych
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register/", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint do rejestracji nowego użytkownika.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    created_user = crud.create_user(db=db, user=user)
    return created_user


@app.get("/")
def read_root():
    return {"message": "Auth Service is running!"}