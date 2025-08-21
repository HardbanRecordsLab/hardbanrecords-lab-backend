# common/models.py - WERSJA Z MODELEM ROYALTY SPLITS
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="music_creator")
    releases = relationship("MusicRelease", back_populates="owner")

class MusicRelease(Base):
    __tablename__ = "music_releases"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    artist = Column(String, index=True, nullable=False)
    status = Column(String, default="draft")
    
    # Przechowuje dodatkowe dane, jak URL-e, gatunek, etc.
    release_meta = Column(JSON) 
    
    # NOWE POLE: Przechowuje informacje o podziale tantiem
    # Przykład: [{"email": "wspoltworca@example.com", "share": 50}, {"email": "drugi@example.com", "share": 50}]
    royalty_splits = Column(JSON) 

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="releases")