# music_app/main.py - KOMPLETNY SERWIS MUZYCZNY
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil
import os
from pathlib import Path

from common.database import SessionLocal
from common import models
from auth_app.crud import get_current_user
from . import crud, schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Folder na pliki audio (tymczasowy - później S3)
UPLOAD_DIR = Path("uploads/audio")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.get("/releases/", response_model=List[schemas.MusicRelease])
def get_my_releases(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Pobiera wszystkie wydania muzyczne aktualnego użytkownika."""
    releases = crud.get_music_releases_by_owner(db, current_user.id, skip, limit)
    return releases

@router.post("/releases/", response_model=schemas.MusicRelease)
def create_release(
    title: str = Form(...),
    artist: str = Form(...),
    genre: str = Form(default="Electronic"),
    audio_file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Tworzy nowe wydanie muzyczne z plikiem audio."""
    
    # Walidacja pliku audio
    if not audio_file.filename.lower().endswith(('.mp3', '.wav', '.flac')):
        raise HTTPException(400, detail="Unsupported audio format. Use MP3, WAV, or FLAC.")
    
    if audio_file.size > 100 * 1024 * 1024:  # 100MB limit
        raise HTTPException(400, detail="File too large. Maximum 100MB.")
    
    # Zapisz plik audio
    file_path = UPLOAD_DIR / f"{current_user.id}_{audio_file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(audio_file.file, buffer)
    
    # Stwórz release w bazie
    release_data = schemas.MusicReleaseCreate(
        title=title,
        artist=artist,
        status="uploaded",
        release_meta={
            "genre": genre,
            "file_path": str(file_path),
            "file_size": audio_file.size,
            "original_filename": audio_file.filename
        }
    )
    
    release = crud.create_music_release(db, release_data, current_user.id)
    return release

@router.get("/releases/{release_id}", response_model=schemas.MusicRelease)
def get_release(
    release_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Pobiera konkretne wydanie muzyczne."""
    release = crud.get_music_release_by_id(db, release_id, current_user.id)
    if not release:
        raise HTTPException(404, detail="Release not found")
    return release

@router.put("/releases/{release_id}", response_model=schemas.MusicRelease)
def update_release(
    release_id: int,
    release_update: schemas.MusicReleaseCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Aktualizuje istniejące wydanie muzyczne."""
    release = crud.update_music_release(db, release_id, current_user.id, release_update)
    if not release:
        raise HTTPException(404, detail="Release not found")
    return release

@router.delete("/releases/{release_id}")
def delete_release(
    release_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Usuwa wydanie muzyczne."""
    success = crud.delete_music_release(db, release_id, current_user.id)
    if not success:
        raise HTTPException(404, detail="Release not found")
    return {"message": "Release deleted successfully"}

@router.post("/releases/{release_id}/distribute")
def distribute_release(
    release_id: int,
    platforms: List[str],
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Dystrybuuje wydanie do wybranych platform (Spotify, Apple Music, etc.)."""
    release = crud.get_music_release_by_id(db, release_id, current_user.id)
    if not release:
        raise HTTPException(404, detail="Release not found")
    
    # TODO: Integracja z RouteNote API
    # Na razie symulujemy proces dystrybucji
    
    # Aktualizuj status
    release.status = "distributing"
    if not release.release_meta:
        release.release_meta = {}
    release.release_meta["distribution_platforms"] = platforms
    release.release_meta["distribution_started"] = "2025-01-01"  # datetime.now().isoformat()
    
    db.commit()
    
    return {
        "message": "Distribution started",
        "release_id": release_id,
        "platforms": platforms,
        "status": "distributing"
    }

@router.get("/stats")
def get_stats(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Zwraca statystyki użytkownika."""
    total_releases = crud.count_user_releases(db, current_user.id)
    published_releases = len(crud.get_releases_by_status(db, current_user.id, "published"))
    
    return {
        "total_releases": total_releases,
        "published_releases": published_releases,
        "draft_releases": total_releases - published_releases,
        "user_id": current_user.id
    }
