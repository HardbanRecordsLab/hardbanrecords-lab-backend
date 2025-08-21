# music_app/crud.py - POPRAWIONA WERSJA
from sqlalchemy.orm import Session
from sqlalchemy import and_
from common import models
from . import schemas
from typing import Optional, List

def get_music_releases_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> List[models.MusicRelease]:
    """
    Pobiera listę wszystkich wydań muzycznych należących do danego użytkownika.
    """
    return (
        db.query(models.MusicRelease)
        .filter(models.MusicRelease.owner_id == owner_id)
        .order_by(models.MusicRelease.id.desc())  # Najnowsze pierwsze
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_music_release_by_id(db: Session, release_id: int, owner_id: int) -> Optional[models.MusicRelease]:
    """
    Pobiera konkretne wydanie muzyczne po ID, sprawdzając czy należy do użytkownika.
    """
    return (
        db.query(models.MusicRelease)
        .filter(
            and_(
                models.MusicRelease.id == release_id,
                models.MusicRelease.owner_id == owner_id
            )
        )
        .first()
    )

def create_music_release(db: Session, release: schemas.MusicReleaseCreate, owner_id: int) -> models.MusicRelease:
    """
    Tworzy nowe wydanie muzyczne w bazie danych dla określonego użytkownika.
    """
    # Konwertujemy Pydantic model na dict, a potem tworzymy SQLAlchemy model
    release_data = release.model_dump()
    
    db_release = models.MusicRelease(
        title=release_data["title"],
        artist=release_data["artist"],
        status=release_data.get("status", "draft"),
        release_meta=release_data.get("release_meta"),
        audio_file_path=release_data.get("audio_file_path"),  # DODANE
        owner_id=owner_id
    )
    
    db.add(db_release)
    db.commit()
    db.refresh(db_release)
    return db_release

def update_music_release(db: Session, release_id: int, owner_id: int, release_update: schemas.MusicReleaseUpdate) -> Optional[models.MusicRelease]:
    """
    Aktualizuje istniejące wydanie muzyczne.
    """
    db_release = get_music_release_by_id(db, release_id, owner_id)
    if not db_release:
        return None
    
    # Aktualizuj tylko pola które zostały podane
    update_data = release_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_release, field, value)
    
    db.commit()
    db.refresh(db_release)
    return db_release

def delete_music_release(db: Session, release_id: int, owner_id: int) -> bool:
    """
    Usuwa wydanie muzyczne z bazy danych.
    Zwraca True jeśli usunięto, False jeśli nie znaleziono.
    """
    db_release = get_music_release_by_id(db, release_id, owner_id)
    if not db_release:
        return False
    
    db.delete(db_release)
    db.commit()
    return True

def get_releases_by_status(db: Session, owner_id: int, status: str) -> List[models.MusicRelease]:
    """
    Pobiera wydania muzyczne o konkretnym statusie dla danego użytkownika.
    Przydatne do filtrowania (np. tylko opublikowane, tylko drafty).
    """
    return (
        db.query(models.MusicRelease)
        .filter(
            and_(
                models.MusicRelease.owner_id == owner_id,
                models.MusicRelease.status == status
            )
        )
        .order_by(models.MusicRelease.id.desc())
        .all()
    )

def count_user_releases(db: Session, owner_id: int) -> int:
    """
    Zlicza ile wydań ma dany użytkownik.
    Przydatne do statystyk i limitów.
    """
    return (
        db.query(models.MusicRelease)
        .filter(models.MusicRelease.owner_id == owner_id)
        .count()
    )

def search_releases(db: Session, owner_id: int, search_term: str) -> List[models.MusicRelease]:
    """
    Wyszukuje wydania po tytule lub artyście.
    """
    search_pattern = f"%{search_term}%"
    return (
        db.query(models.MusicRelease)
        .filter(
            and_(
                models.MusicRelease.owner_id == owner_id,
                (
                    models.MusicRelease.title.ilike(search_pattern) |
                    models.MusicRelease.artist.ilike(search_pattern)
                )
            )
        )
        .order_by(models.MusicRelease.id.desc())
        .all()
    )