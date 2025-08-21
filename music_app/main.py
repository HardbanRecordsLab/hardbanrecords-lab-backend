# music_app/main.py - POPRAWIONA WERSJA Z WŁAŚCIWYMI SCHEMATAMI
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from file_storage.s3_handler import S3Handler
from common.database import SessionLocal
from common import models
from auth_app.crud import get_current_user
from . import crud, schemas

router = APIRouter()
s3_handler = S3Handler()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/releases/", response_model=schemas.MusicRelease)
async def create_release(
    title: str = Form(...),
    artist: str = Form(...),
    genre: str = Form(default="Electronic"),
    audio_file: UploadFile = File(...),
    cover_art_file: Optional[UploadFile] = File(None), # Nowy, opcjonalny parametr
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Tworzy nowe wydanie, wysyłając plik audio i okładkę do chmury S3."""
    # Walidacja audio
    if not audio_file.filename.lower().endswith(('.mp3', '.wav', '.flac')):
        raise HTTPException(status_code=400, detail="Nieobsługiwany format audio.")
    
    # Walidacja okładki (jeśli została dodana)
    if cover_art_file and not cover_art_file.content_type.startswith('image/'):
         raise HTTPException(status_code=400, detail="Plik okładki musi być obrazem.")

    # Tworzymy wstępny wpis w bazie, aby uzyskać release.id
    pre_release_data = schemas.MusicReleaseCreate(
        title=title, artist=artist, status="pending_upload", release_meta={"genre": genre}
    )
    release = crud.create_music_release(db=db, release=pre_release_data, owner_id=current_user.id)
    
    # Wysyłamy plik audio
    audio_url = await s3_handler.upload_audio_file(
        file=audio_file, user_id=current_user.id, release_id=release.id
    )
    if not audio_url:
        crud.delete_music_release(db, release_id=release.id, owner_id=current_user.id)
        raise HTTPException(status_code=500, detail="Nie udało się wysłać pliku audio.")

    # Wysyłamy okładkę, jeśli została dołączona
    cover_art_url = None
    if cover_art_file:
        cover_art_url = await s3_handler.upload_cover_art(
            file=cover_art_file, user_id=current_user.id, release_id=release.id
        )
        if not cover_art_url:
            # W razie błędu okładki, kontynuujemy, ale logujemy błąd. Można też przerwać.
            print(f"Ostrzeżenie: Nie udało się wysłać okładki dla wydania ID: {release.id}")

    # Aktualizujemy wpis w bazie o wszystkie URL-e i zmieniamy status
    release.status = "uploaded"
    release.release_meta.update({
        "audio_file_url": audio_url,
        "cover_art_url": cover_art_url,
        "file_size": audio_file.size,
        "original_filename": audio_file.filename
    })
    db.commit()
    db.refresh(release)
    
    return release

@router.get("/releases/", response_model=List[schemas.MusicRelease])
def get_my_releases(
    skip: int = 0, 
    limit: int = 100, 
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    releases = crud.get_music_releases_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)
    return releases

@router.get("/releases/{release_id}", response_model=schemas.MusicRelease)
def get_release(
    release_id: int, 
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    release = crud.get_music_release_by_id(db, release_id=release_id, owner_id=current_user.id)
    if not release:
        raise HTTPException(status_code=404, detail="Release not found")
    return release

# POPRAWIONO - używamy teraz MusicReleaseUpdate zamiast MusicReleaseCreate
@router.put("/releases/{release_id}", response_model=schemas.MusicRelease)
def update_release(
    release_id: int, 
    release_update: schemas.MusicReleaseUpdate,  # ZMIENIONO Z MusicReleaseCreate
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    release = crud.update_music_release(db, release_id=release_id, owner_id=current_user.id, release_update=release_update)
    if not release:
        raise HTTPException(status_code=404, detail="Release not found")
    return release

@router.delete("/releases/{release_id}")
def delete_release(
    release_id: int, 
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    success = crud.delete_music_release(db, release_id=release_id, owner_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Release not found")
    return {"message": "Release deleted successfully"}

@router.get("/stats")
def get_stats(
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    total_releases = crud.count_user_releases(db, owner_id=current_user.id)
    published_releases = len(crud.get_releases_by_status(db, owner_id=current_user.id, status="published"))
    return {
        "total_releases": total_releases, 
        "published_releases": published_releases, 
        "draft_releases": total_releases - published_releases, 
        "user_id": current_user.id
    }
