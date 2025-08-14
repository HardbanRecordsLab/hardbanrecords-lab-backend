# music_app/main.py

# Krok 1: Importujemy potrzebne narzędzia

from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import sys
import os

# Krok 2: Poprawka ścieżki, aby Python widział nasze inne foldery (common, auth\_app)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(**file**))))

# Krok 3: Importujemy nasze własne moduły

from common import models

# WAŻNE: Importujemy funkcje do autoryzacji i bazy danych z naszego 'auth\_app'

from auth\_app.crud import get\_current\_user, get\_db
from . import crud, schemas

# Krok 4: Inicjalizacja aplikacji i routera

app = FastAPI()
router = APIRouter()

# Krok 5: Endpoint do tworzenia nowego wydania muzycznego (CHRONIONY)

@router.post("/", response\_model=schemas.MusicRelease, tags=["Music Releases"])
def create\_release\_for\_user(
release: schemas.MusicReleaseCreate,
db: Session = Depends(get\_db),
current\_user: models.User = Depends(get\_current\_user)
):
"""
Tworzy nowe wydanie muzyczne dla aktualnie zalogowanego użytkownika.
Wymaga ważnego tokena JWT w nagłówku Authorization.
"""
return crud.create\_music\_release(db=db, release=release, owner\_id=current\_user.id)

# Krok 6: Endpoint do pobierania listy wydań muzycznych (CHRONIONY)

@router.get("/", response\_model=List[schemas.MusicRelease], tags=["Music Releases"])
def read\_user\_releases(
skip: int = 0,
limit: int = 100,
db: Session = Depends(get\_db),
current\_user: models.User = Depends(get\_current\_user)
):
"""
Pobiera listę wydań muzycznych dla aktualnie zalogowanego użytkownika.
Wymaga ważnego tokena JWT w nagłówku Authorization.
"""
releases = crud.get\_music\_releases\_by\_owner(db, owner\_id=current\_user.id, skip=skip, limit=limit)
return releases

# Krok 7: Podłączenie routera do aplikacji

app.include\_router(router)