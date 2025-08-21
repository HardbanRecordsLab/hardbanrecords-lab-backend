# Pełny, samowystarczalny kod do umieszczenia w routerze modułu muzycznego
import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile
from sqlalchemy.orm import Session
from typing import List

# Założenie, że masz takie pliki i strukturę. Dostosuj importy do swojego projektu.
from ..database import get_db
from . import schemas, models
from ..auth_app import oauth2

# Definicja ścieżki do folderu, gdzie będą przechowywane pliki
UPLOAD_DIRECTORY = "uploads"

# Inicjalizacja routera API
router = APIRouter(
    prefix="/music/releases",
    tags=["Music Releases"]
)

# === NOWY ENDPOINT DO TWORZENIA WYDANIA ===

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ReleaseOut)
def create_release(
    title: str = Form(...),
    artist: str = Form(...),
    cover_image: UploadFile = Form(...),
    audio_file: UploadFile = Form(...),
    db: Session = Depends(get_db),
    # Zabezpieczenie: Wymaga, aby użytkownik był zalogowany.
    # Pobiera ID użytkownika z tokenu JWT.
    current_user_id: int = Depends(oauth2.get_current_user_id)
):
    """
    Endpoint do tworzenia nowego wydania muzycznego.

    Przyjmuje dane formularza multipart/form-data, w tym pliki.
    1. Tworzy folder `uploads`, jeśli nie istnieje.
    2. Zapisuje plik okładki i plik audio na serwerze.
    3. Tworzy nowy rekord w bazie danych.
    4. Zwraca utworzony obiekt wydania.
    """
    # Krok 1: Walidacja i przygotowanie ścieżek do zapisu plików
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

    cover_image_path = os.path.join(UPLOAD_DIRECTORY, cover_image.filename)
    audio_file_path = os.path.join(UPLOAD_DIRECTORY, audio_file.filename)

    # Krok 2: Zapisanie plików na dysku serwera
    try:
        with open(cover_image_path, "wb") as buffer:
            shutil.copyfileobj(cover_image.file, buffer)
        with open(audio_file_path, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)
    except Exception as e:
        # W przypadku błędu zapisu, zgłoś wyjątek
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Nie udało się zapisać plików na serwerze: {e}"
        )
    finally:
        # Zawsze zamykaj pliki po operacji
        cover_image.file.close()
        audio_file.file.close()

    # Krok 3: Stworzenie nowego obiektu w bazie danych
    # Zakładamy, że model `Release` ma pole `owner_id` do powiązania z użytkownikiem.
    new_release_data = {
        "title": title,
        "artist": artist,
        "cover_image_url": cover_image_path, # Zapisujemy ścieżkę do pliku
        "audio_file_url": audio_file_path,   # Zapisujemy ścieżkę do pliku
        "owner_id": current_user_id
    }
    new_release = models.Release(**new_release_data)

    db.add(new_release)
    db.commit()
    db.refresh(new_release)

    # Krok 4: Zwrócenie utworzonego obiektu
    return new_release


# Przykładowy, istniejący endpoint do pobierania listy wydań (dla kontekstu)
@router.get("/", response_model=List[schemas.ReleaseOut])
def get_releases(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(oauth2.get_current_user_id)
):
    """
    Endpoint do pobierania listy wydawnictw należących do zalogowanego użytkownika.
    """
    releases = db.query(models.Release).filter(models.Release.owner_id == current_user_id).all()
    return releases