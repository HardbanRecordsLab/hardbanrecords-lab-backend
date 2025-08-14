# common/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="book_author", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacja: Jeden użytkownik może mieć wiele wydań muzycznych
    music_releases = relationship("MusicRelease", back_populates="owner")

# --- NOWA KLASA: WYDANIE MUZYCZNE ---
class MusicRelease(Base):
    __tablename__ = "music_releases"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    artist = Column(String, index=True, nullable=False)
    
    # Używamy typu JSON do przechowywania elastycznych metadanych
    # np. gatunek, data wydania, kody ISRC/UPC
    metadata = Column(JSON)
    
    # Klucz do pliku audio w chmurze (np. S3)
    s3_audio_key = Column(String)
    # Klucz do pliku okładki w chmurze
    s3_cover_art_key = Column(String)
    
    status = Column(String, default="draft") # np. 'draft', 'in_review', 'published'
    
    # Klucz obcy łączący wydanie z jego właścicielem (użytkownikiem)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Relacja: To wydanie należy do jednego właściciela (użytkownika)
    owner = relationship("User", back_populates="music_releases")
