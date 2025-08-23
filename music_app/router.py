from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile
from sqlalchemy.orm import Session
from typing import List

# Importujemy naszą klasę S3Handler
from file_storage.s3_handler import S3Handler

# Importy specyficzne dla Twojej aplikacji
from common.database import get_db
from . import crud, schemas
from auth_app.main import get_current_user_id

router = APIRouter(
    prefix="/releases", # Zgodnie z Twoją strukturą, prefix jest w `main.py`
    tags=["Music Releases"]
)

# Inicjalizujemy handler S3 raz, aby można go było używać w całym module
s3_handler = S3Handler()

@router.post("/", response_model=schemas.MusicRelease, status_code=status.HTTP_201_CREATED)
def create_release(
    db: Session = Depends(get_db),
    title: str = Form(...),
    artist: str = Form(...),
    cover_image: UploadFile = Form(...),
    audio_file: UploadFile = Form(...),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Tworzy nowe wydanie muzyczne, przesyłając pliki bezpośrednio do AWS S3.
    """
    # Krok 1: Prześlij pliki do S3 używając naszego handlera
    cover_image_url = s3_handler.upload_file(
        file_obj=cover_image.file,
        folder="covers",
        original_filename=cover_image.filename
    )
    audio_file_url = s3_handler.upload_file(
        file_obj=audio_file.file,
        folder="audio",
        original_filename=audio_file.filename
    )

    # Sprawdzenie, czy przesyłanie się powiodło
    if not cover_image_url or not audio_file_url:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Nie udało się przesłać jednego z plików do chmury."
        )

    # Krok 2: Przygotuj dane do zapisu w bazie
    release_data = schemas.MusicReleaseCreate(
        title=title,
        artist=artist,
        cover_image_url=cover_image_url,
        audio_file_url=audio_file_url,
        owner_id=current_user_id
    )
    
    # Krok 3: Zapisz wydanie w bazie danych
    return crud.create_music_release(db=db, release=release_data)


@router.get("/", response_model=List[schemas.MusicRelease])
def read_releases(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Pobiera listę wydawnictw dla zalogowanego użytkownika.
    """
    releases = crud.get_music_releases_by_owner(db, owner_id=current_user_id, skip=skip, limit=limit)
    return releases