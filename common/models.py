# Pełna zawartość do wklejenia do pliku: common/models.py

from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum, ForeignKey
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
    role = Column(SQLAlchemyEnum(UserRole), nullable=False)
    releases = relationship("Release", back_populates="owner")

class Release(Base):
    __tablename__ = 'releases'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    artist = Column(String, index=True)
    audio_file_path = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="releases")