# music_app/schemas.py - KOMPLETNA POPRAWIONA WERSJA
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Any

# Nowy schemat definiujący pojedynczy wpis podziału tantiem
class RoyaltySplit(BaseModel):
    email: EmailStr
    share: int # Procent, np. 50

# Schemat bazowy dla wydania muzycznego
class MusicReleaseBase(BaseModel):
    title: str
    artist: str
    status: Optional[str] = "draft"
    release_meta: Optional[dict] = {}
    royalty_splits: Optional[List[RoyaltySplit]] = [] # Dodajemy pole do schematu

# Schemat używany przy tworzeniu nowego wydania
class MusicReleaseCreate(MusicReleaseBase):
    pass

# DODANA BRAKUJĄCA KLASA - Schemat używany przy aktualizacji wydania
class MusicReleaseUpdate(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    status: Optional[str] = None
    release_meta: Optional[dict] = None
    royalty_splits: Optional[List[RoyaltySplit]] = None
    audio_file_path: Optional[str] = None
    
    class Config:
        from_attributes = True

# Schemat używany przy zwracaniu danych z API (zawiera ID)
class MusicRelease(MusicReleaseBase):
    id: int
    owner_id: int
    audio_file_path: Optional[str] = None

    class Config:
        from_attributes = True # Zmieniono z `orm_mode` na `from_attributes` dla Pydantic v2