# common/models.py - POPRAWIONA WERSJA

from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from .database import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MUSIC_CREATOR = "music_creator"
    BOOK_AUTHOR = "book_author"
    ELEARNING_INSTRUCTOR = "e-learning_instructor"

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLAlchemyEnum(UserRole), nullable=False, default=UserRole.MUSIC_CREATOR)
    
    # Relacje
    releases = relationship("MusicRelease", back_populates="owner")

class MusicRelease(Base):
    __tablename__ = 'releases'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    artist = Column(String, index=True, nullable=False)
    status = Column(String, default="draft", nullable=False)
    
    # DODANE: Pole dla ścieżki do pliku audio
    audio_file_path = Column(String, nullable=True)
    
    # Metadane jako JSON
    release_meta = Column(JSON, nullable=True)
    
    # Klucz obcy do User
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Relacja do User
    owner = relationship("User", back_populates="releases")

# Alias dla kompatybilności wstecznej
Release = MusicRelease