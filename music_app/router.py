# music_app/router.py

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Annotated

from .. import database
from . import schemas, crud, models
from ..auth_app.oauth2 import get_current_user_id # Założenie: funkcja do pobierania ID usera
from ..file_storage.s3_handler import s3_upload # Założenie: funkcja do uploadu na S3

# Inicjalizacja routera dla modułu muzycznego.
router = APIRouter(
    prefix="/music",
    tags=["Music Releases"]
)

@router.post("/releases/", response_model=schemas.MusicReleaseOut, status_code=status.HTTP_201_CREATED)
def create_new_release(
    title: Annotated[str, Form()],
    artist: Annotated[str, Form()],
    cover_image: Annotated[UploadFile, File()],
    audio_file: Annotated[UploadFile, File()],
    db: Session = Depends(database.get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Endpoint do tworzenia nowego wydawnictwa muzycznego z plikami."""
    # Przesyłanie plików na S3
    cover_url = s3_upload(cover_image, "covers")
    audio_url = s3_upload(audio_file, "audio")

    # Zapis metadanych w bazie danych
    return crud.create_music_release(
        db=db,
        title=title,
        artist=artist,
        cover_url=cover_url,
        audio_url=audio_url,
        owner_id=current_user_id
    )

@router.get("/releases/", response_model=List[schemas.MusicReleaseOut])
def get_user_releases(
    db: Session = Depends(database.get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Pobiera listę wszystkich wydawnictw należących do zalogowanego użytkownika."""
    return crud.get_music_releases_by_owner(db, owner_id=current_user_id)

# NOWY ENDPOINT DO ZARZĄDZANIA ROYALTY SPLITS
@router.post("/releases/{release_id}/royalty-splits", response_model=schemas.RoyaltySplitOut, status_code=status.HTTP_201_CREATED)
def add_royalty_split_to_release(
    release_id: int,
    split_data: schemas.RoyaltySplitCreate,
    db: Session = Depends(database.get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Endpoint API do dodawania nowego podziału tantiem do istniejącego wydawnictwa.

    - Wymaga uwierzytelnienia (przez `get_current_user_id`).
    - Przyjmuje ID wydawnictwa w ścieżce URL.
    - Przyjmuje dane podziału (email, procent) w ciele żądania.
    - Wywołuje funkcję z warstwy CRUD, która zawiera całą logikę walidacyjną.
    [cite_start][cite: 215-221]
    """
    return crud.create_royalty_split_for_release(
        db=db,
        split_data=split_data,
        release_id=release_id,
        owner_id=current_user_id
    )