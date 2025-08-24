# music_app/models.py

from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Numeric
from sqlalchemy.orm import relationship
# POPRAWIONY IMPORT: Importujemy 'Base' z centralnej lokalizacji
from common.database import Base

class MusicRelease(Base):
    __tablename__ = 'music_releases'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    cover_image_url = Column(String, nullable=False)
    audio_file_url = Column(String, nullable=False)
    status = Column(String, default='pending', nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Ta relacja nie wymaga zmiany, bo odwołuje się do klasy User,
    # a SQLAlchemy samo znajduje odpowiednią tabelę.
    owner = relationship("User")
    royalty_splits = relationship("MusicReleaseRoyaltySplit", back_populates="release", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<MusicRelease(id={self.id}, title='{self.title}', artist='{self.artist}')>"

class MusicReleaseRoyaltySplit(Base):
    __tablename__ = 'music_release_royalty_splits'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)
    share_percentage = Column(Numeric(5, 2), nullable=False)
    release_id = Column(Integer, ForeignKey('music_releases.id'), nullable=False)
    release = relationship("MusicRelease", back_populates="royalty_splits")

    def __repr__(self):
        return f"<MusicReleaseRoyaltySplit(id={self.id}, release_id={self.release_id}, email='{self.email}', share={self.share_percentage}%)>"