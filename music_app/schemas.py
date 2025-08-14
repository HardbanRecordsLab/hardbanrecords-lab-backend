# music_app/schemas.py
from pydantic import BaseModel
from typing import Optional, Dict, Any

class MusicReleaseBase(BaseModel):
    title: str
    artist: str
    status: Optional[str] = "draft"
    # ZMIANA: Zmieniamy nazwę z 'metadata' na 'release_meta'
    release_meta: Optional[Dict[str, Any]] = None

class MusicReleaseCreate(MusicReleaseBase):
    pass

class MusicRelease(MusicReleaseBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
