# music_app/schemas.py - POPRAWIONA WERSJA
from pydantic import BaseModel
from typing import Optional, Dict, Any

class MusicReleaseBase(BaseModel):
    title: str
    artist: str
    status: Optional[str] = "draft"
    audio_file_path: Optional[str] = None  # DODANE
    release_meta: Optional[Dict[str, Any]] = None

class MusicReleaseCreate(MusicReleaseBase):
    """Schemat do tworzenia nowego wydania."""
    pass

class MusicReleaseUpdate(BaseModel):
    """Schemat do aktualizacji wydania - wszystkie pola opcjonalne."""
    title: Optional[str] = None
    artist: Optional[str] = None
    status: Optional[str] = None
    audio_file_path: Optional[str] = None
    release_meta: Optional[Dict[str, Any]] = None

class MusicRelease(MusicReleaseBase):
    """Schemat zwracający pełne dane wydania."""
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class MusicReleaseList(BaseModel):
    """Schemat do zwracania listy wydań z metadanymi."""
    items: list[MusicRelease]
    total: int
    skip: int
    limit: int