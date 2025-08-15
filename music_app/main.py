# music_app/main.py
from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from common import models
from common.database import SessionLocal, engine, Base
from auth_app.crud import get_current_user, get_db
from . import crud, schemas

# Tworzymy tabele w bazie danych
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HardbanRecords Music Service",
    description="Music release management for independent artists",
    version="1.0.0"
)

router = APIRouter(prefix="/music", tags=["Music Releases"])

@router.get("/", response_model=List[schemas.MusicRelease])
def get_my_releases(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Pobiera listę wszystkich wydań muzycznych zalogowanego użytkownika.
    """
    releases = crud.get_music_releases_by_owner(db, current_user.id, skip, limit)
    return releases

@router.post("/", response_model=schemas.MusicRelease, status_code=status.HTTP_201_CREATED)
def create_release(
    release: schemas.MusicReleaseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Tworzy nowe wydanie muzyczne dla zalogowanego użytkownika.
    """
    # Sprawdź czy użytkownik ma uprawnienia do tworzenia muzyki
    if current_user.role not in ["music_creator", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only music creators can create releases"
        )
    
    return crud.create_music_release(db, release, current_user.id)

@router.get("/{release_id}", response_model=schemas.MusicRelease)
def get_release(
    release_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Pobiera szczegóły konkretnego wydania muzycznego.
    Użytkownik może zobaczyć tylko swoje wydania.
    """
    release = db.query(models.MusicRelease).filter(
        models.MusicRelease.id == release_id,
        models.MusicRelease.owner_id == current_user.id
    ).first()
    
    if not release:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Release not found or access denied"
        )
    return release

@router.put("/{release_id}", response_model=schemas.MusicRelease)
def update_release(
    release_id: int,
    release_update: schemas.MusicReleaseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Aktualizuje istniejące wydanie muzyczne.
    """
    # Sprawdź czy wydanie istnieje i należy do użytkownika
    db_release = db.query(models.MusicRelease).filter(
        models.MusicRelease.id == release_id,
        models.MusicRelease.owner_id == current_user.id
    ).first()
    
    if not db_release:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Release not found"
        )
    
    # Aktualizuj pola
    for field, value in release_update.model_dump(exclude_unset=True).items():
        setattr(db_release, field, value)
    
    db.commit()
    db.refresh(db_release)
    return db_release

@router.delete("/{release_id}")
def delete_release(
    release_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Usuwa wydanie muzyczne.
    """
    release = db.query(models.MusicRelease).filter(
        models.MusicRelease.id == release_id,
        models.MusicRelease.owner_id == current_user.id
    ).first()
    
    if not release:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Release not found"
        )
    
    db.delete(release)
    db.commit()
    return {"message": "Release deleted successfully"}

@router.get("/health")
def health_check():
    """
    Sprawdza czy serwis muzyczny działa poprawnie.
    """
    return {"status": "Music Service is running!", "service": "music_app"}

# Dodaj router do głównej aplikacji
app.include_router(router)

# Endpoint główny dla serwisu
@app.get("/")
def read_root():
    return {
        "message": "HardbanRecords Music Service", 
        "version": "1.0.0",
        "docs": "/docs"
    }