from sqlalchemy.orm import Session
from common import models
from . import schemas

def get_music_releases_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    """
    Pobiera listę wszystkich wydań muzycznych należących do danego użytkownika.
    """
    return db.query(models.MusicRelease).filter(models.MusicRelease.owner_id == owner_id).offset(skip).limit(limit).all()

def create_music_release(db: Session, release: schemas.MusicReleaseCreate, owner_id: int):
    """
    Tworzy nowe wydanie muzyczne w bazie danych dla określonego użytkownika.
    """
    db_release = models.MusicRelease(
        **release.model_dump(),
        owner_id=owner_id
    )
    db.add(db_release)
    db.commit()
    db.refresh(db_release)
    return db_release