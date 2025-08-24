# music_app/crud.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas
from fastapi import HTTPException, status
from decimal import Decimal

# Tutaj powinny znajdować się Twoje istniejące funkcje CRUD,
# np. create_music_release, get_releases_by_owner_id, itp.
# Poniżej dodajemy nową funkcję.

def get_music_release(db: Session, release_id: int):
    """Pobiera pojedyncze wydawnictwo po ID."""
    return db.query(models.MusicRelease).filter(models.MusicRelease.id == release_id).first()

def get_music_releases_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    """Pobiera listę wydawnictw dla danego właściciela."""
    return db.query(models.MusicRelease).filter(models.MusicRelease.owner_id == owner_id).offset(skip).limit(limit).all()

def create_music_release(db: Session, title: str, artist: str, cover_url: str, audio_url: str, owner_id: int):
    """Tworzy nowy wpis wydawnictwa muzycznego w bazie danych."""
    db_release = models.MusicRelease(
        title=title,
        artist=artist,
        cover_image_url=cover_url,
        audio_file_url=audio_url,
        owner_id=owner_id
    )
    db.add(db_release)
    db.commit()
    db.refresh(db_release)
    return db_release

# NOWA FUNKCJA DO OBSŁUGI ROYALTY SPLITS
def create_royalty_split_for_release(db: Session, split_data: schemas.RoyaltySplitCreate, release_id: int, owner_id: int):
    """
    Tworzy nowy wpis podziału tantiem dla konkretnego wydawnictwa.
    Zawiera kluczową logikę biznesową, sprawdzającą czy suma udziałów
    nie przekracza 100%, co jest fundamentalnym wymaganiem tej funkcjonalności.
    [cite_start][cite: 220]
    """
    # Krok 1: Weryfikacja. Sprawdź, czy wydawnictwo istnieje i czy
    # zalogowany użytkownik jest jego właścicielem.
    release = db.query(models.MusicRelease).filter(
        models.MusicRelease.id == release_id,
        models.MusicRelease.owner_id == owner_id
    ).first()

    if not release:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Wydawnictwo o ID {release_id} nie zostało znalezione lub nie masz uprawnień do jego modyfikacji."
        )

    # Krok 2: Obliczenie. Zsumuj wszystkie istniejące już udziały dla tego wydawnictwa.
    # Używamy `Decimal` dla precyzji.
    total_share = db.query(func.sum(models.MusicReleaseRoyaltySplit.share_percentage)).filter(
        models.MusicReleaseRoyaltySplit.release_id == release_id
    ).scalar() or Decimal('0.0')

    # Krok 3: Walidacja. Sprawdź, czy dodanie nowego udziału nie przekroczy 100%.
    if total_share + Decimal(str(split_data.share_percentage)) > Decimal('100.0'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Nie można dodać podziału. Suma udziałów przekroczyłaby 100%. Obecna suma: {total_share}%."
        )

    # Krok 4: Utworzenie i zapis. Stwórz nowy obiekt i zapisz go w bazie.
    db_split = models.MusicReleaseRoyaltySplit(
        email=split_data.email,
        share_percentage=Decimal(str(split_data.share_percentage)),
        release_id=release_id
    )
    db.add(db_split)
    db.commit()
    db.refresh(db_split)
    return db_split