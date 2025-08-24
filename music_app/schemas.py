# music_app/schemas.py

from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

# --- NOWE SCHEMATY DLA ROYALTY SPLITS ---

class RoyaltySplitBase(BaseModel):
    """Podstawowy schemat dla podziału tantiem."""
    email: EmailStr
    # Definiujemy walidację: udział musi być liczbą > 0 i <= 100.
    share_percentage: float = Field(..., gt=0, le=100, description="Udział procentowy musi być większy od 0 i mniejszy lub równy 100.")

class RoyaltySplitCreate(RoyaltySplitBase):
    """Schemat używany do walidacji danych przychodzących przy tworzeniu nowego podziału."""
    pass

class RoyaltySplitOut(RoyaltySplitBase):
    """Schemat używany do zwracania danych o podziale tantiem z API. Zawiera dodatkowo ID."""
    id: int

    class Config:
        # Pozwala Pydantic na konwersję z modelu SQLAlchemy.
        from_attributes = True

# --- ZAKTUALIZOWANE SCHEMATY DLA MUSIC RELEASE ---

class MusicReleaseBase(BaseModel):
    """Podstawowy schemat dla wydawnictwa muzycznego."""
    title: str
    artist: str

class MusicReleaseCreate(MusicReleaseBase):
    """Schemat używany do tworzenia wydawnictwa (jeśli dane idą w ciele JSON)."""
    pass

class MusicReleaseOut(MusicReleaseBase):
    """
    Zaktualizowany schemat wyjściowy dla wydawnictwa.
    Teraz zawiera również listę wszystkich przypisanych do niego podziałów tantiem.
    """
    id: int
    cover_image_url: str
    audio_file_url: str
    status: str
    created_at: datetime
    owner_id: int
    
    # Dodane pole, które będzie zawierać listę obiektów RoyaltySplitOut.
    royalty_splits: List[RoyaltySplitOut] = [] 

    class Config:
        from_attributes = True