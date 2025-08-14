# music_app/crud.py
from sqlalchemy.orm import Session
from common import models
from . import schemas

def get\_music\_releases\_by\_owner(db: Session, owner\_id: int, skip: int = 0, limit: int = 100):
"""
Pobiera listę wszystkich wydań muzycznych należących do danego użytkownika.
"""
return db.query(models.MusicRelease).filter(models.MusicRelease.owner\_id == owner\_id).offset(skip).limit(limit).all()

def create\_music\_release(db: Session, release: schemas.MusicReleaseCreate, owner\_id: int):
"""
Tworzy nowe wydanie muzyczne w bazie danych dla określonego użytkownika.
"""
\# Tworzymy obiekt modelu SQLAlchemy na podstawie danych z "formularza" API
db\_release = models.MusicRelease(
\*\*release.model\_dump(),
owner\_id=owner\_id
)