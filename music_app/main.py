# music_app/main.py - WERSJA ZINTEGROWANA Z CHMURĄ S3
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List

# Importujemy nasz nowy handler S3
from file_storage.s3_handler import S3Handler

from common.database import SessionLocal
from common import models
from auth_app.crud import get_current_user
from . import crud, schemas

router = APIRouter()
s3_handler = S3Handler() # Tworzymy instancję handlera

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/releases/", response_model=List[schemas.MusicRelease])
def get_my_releases(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Pobiera wszystkie wydania muzyczne aktualnego użytkownika."""
    releases = crud.get_music_releases_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)
    return releases

@router.post("/releases/", response_model=schemas.MusicRelease)
async def create_release(
    title: str = Form(...),
    artist: str = Form(...),
    genre: str = Form(default="Electronic"),
    audio_file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Tworzy nowe wydanie muzyczne, wysyłając plik audio do chmury S3."""
    # Walidacja pliku audio
    if not audio_file.filename.lower().endswith(('.mp3', '.wav', '.flac')):
        raise HTTPException(status_code=400, detail="Unsupported audio format. Use MP3, WAV, or FLAC.")
    if audio_file.size > 100 * 1024 * 1024:  # 100MB limit
        raise HTTPException(status_code=400, detail="File too large. Maximum 100MB.")

    # Najpierw tworzymy wpis w bazie, aby uzyskać release.id
    pre_release_data = schemas.MusicReleaseCreate(
        title=title, artist=artist, status="pending_upload", release_meta={"genre": genre}
    )
    release = crud.create_music_release(db=db, release=pre_release_data, owner_id=current_user.id)
    
    # Teraz wysyłamy plik do chmury, używając ID z bazy danych
    file_url = await s3_handler.upload_audio_file(
        file=audio_file, user_id=current_user.id, release_id=release.id
    )

    if not file_url:
        # Jeśli upload się nie udał, usuwamy wstępny wpis z bazy
        crud.delete_music_release(db, release_id=release.id, owner_id=current_user.id)
        raise HTTPException(status_code=500, detail="Nie udało się wysłać pliku do chmury.")

    # Aktualizujemy wpis w bazie o URL pliku i zmieniamy status
    release.status = "uploaded"
    release.release_meta.update({
        "file_url": file_url,
        "file_size": audio_file.size,
        "original_filename": audio_file.filename
    })
    db.commit()
    db.refresh(release)
    
    return release

# ... (reszta endpointów: get_release, update_release, delete_release, get_stats - pozostaje bez zmian) ...

@router.get("/releases/{release_id}", response_model=schemas.MusicRelease)
def get_release(release_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    release = crud.get_music_release_by_id(db, release_id=release_id, owner_id=current_user.id)
    if not release:
        raise HTTPException(status_code=404, detail="Release not found")
    return release

@router.put("/releases/{release_id}", response_model=schemas.MusicRelease)
def update_release(release_id: int, release_update: schemas.MusicReleaseCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    release = crud.update_music_release(db, release_id=release_id, owner_id=current_user.id, release_update=release_update)
    if not release:
        raise HTTPException(status_code=404, detail="Release not found")
    return release

@router.delete("/releases/{release_id}")
def delete_release(release_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    success = crud.delete_music_release(db, release_id=release_id, owner_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Release not found")
    return {"message": "Release deleted successfully"}

@router.get("/stats")
def get_stats(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    total_releases = crud.count_user_releases(db, owner_id=current_user.id)
    published_releases = len(crud.get_releases_by_status(db, owner_id=current_user.id, status="published"))
    return {"total_releases": total_releases, "published_releases": published_releases, "draft_releases": total_releases - published_releases, "user_id": current_user.id}