# music_app/models.py

from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from ..database import Base # Założenie: Base jest importowane z pliku np. common/database.py

class MusicRelease(Base):
    """
    Model SQLAlchemy reprezentujący tabelę 'music_releases'.
    Przechowuje metadane dla każdego wydawnictwa muzycznego.
    [cite_start][cite: 678-689]
    """
    __tablename__ = 'music_releases'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    cover_image_url = Column(String, nullable=False)
    audio_file_url = Column(String, nullable=False)
    status = Column(String, default='pending', nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    owner = relationship("User")

    # NOWA RELACJA: Definiuje połączenie jeden-do-wielu z modelem podziału tantiem.
    # Usunięcie wydawnictwa spowoduje automatyczne usunięcie wszystkich
    # powiązanych z nim podziałów dzięki opcji cascade.
    [cite_start]# [cite: 215-221]
    royalty_splits = relationship("MusicReleaseRoyaltySplit", back_populates="release", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<MusicRelease(id={self.id}, title='{self.title}', artist='{self.artist}')>"

# NOWY MODEL: Tabela przechowująca informacje o podziale zysków.
class MusicReleaseRoyaltySplit(Base):
    """
    Model SQLAlchemy reprezentujący tabelę 'music_release_royalty_splits'.
    Przechowuje informacje o podziale procentowym tantiem dla danego
    wydawnictwa muzycznego między zdefiniowanymi współtwórcami.
    [cite_start][cite: 215-221]
    """
    __tablename__ = 'music_release_royalty_splits'

    id = Column(Integer, primary_key=True, index=True)
    
    # Adres e-mail współtwórcy, który ma otrzymać udział.
    email = Column(String, index=True, nullable=False)
    
    # Udział procentowy. Typ Numeric zapewnia precyzję niezbędną
    # przy operacjach finansowych. Przechowuje wartości z dokładnością
    # do dwóch miejsc po przecinku (np. 50.50).
    share_percentage = Column(Numeric(5, 2), nullable=False)
    
    # Klucz obcy łączący ten wpis z konkretnym wydawnictwem muzycznym.
    release_id = Column(Integer, ForeignKey('music_releases.id'), nullable=False)
    
    # Relacja zwrotna, aby z poziomu podziału mieć łatwy dostęp
    # do obiektu nadrzędnego wydawnictwa.
    release = relationship("MusicRelease", back_populates="royalty_splits")

    def __repr__(self):
        return f"<MusicReleaseRoyaltySplit(id={self.id}, release_id={self.release_id}, email='{self.email}', share={self.share_percentage}%)>"