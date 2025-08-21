# music_app/schemas.py - WERSJA ZE SCHEMATAMI ROYALTY SPLITS
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

# Schemat używany przy zwracaniu danych z API (zawiera ID)
class MusicRelease(MusicReleaseBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True # Zmieniono z `orm_mode` na `from_attributes` dla Pydantic v2