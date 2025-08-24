# music_app/router.py

from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Annotated

# POPRAWIONY IMPORT
from common import database
from . import schemas, crud
from auth_app.oauth2 import get_current_user_id 
from file_storage.s3_handler import s3_upload

router = APIRouter(
    prefix="/music",
    tags=["Music Releases"]
)

# ... (reszta kodu bez zmian, ponieważ importy były już poprawne)
# Poniżej dla pewności wklejam cały plik
@router.post("/releases/", response_model=schemas.MusicReleaseOut, status_code=201)
def create_new_release(
    title: Annotated[str, Form()],
    artist: Annotated[str, Form()],
    cover_image: Annotated[UploadFile, File()],
    audio_file: Annotated[UploadFile, File()],
    db: Session = Depends(database.get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    cover_url = s3_upload(cover_image, "covers")
    audio_url = s3_upload(audio_file, "audio")
    return crud.create_music_release(
        db=db,
        title=title,
        artist=artist,
        cover_url=cover_url,
        audio_url=audio_url,
        owner_id=current_user_id
    )

@router.get("/releases/", response_model=List[schemas.MusicReleaseOut])
def get_user_releases(
    db: Session = Depends(database.get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    return crud.get_music_releases_by_owner(db, owner_id=current_user_id)

@router.post("/releases/{release_id}/royalty-splits", response_model=schemas.RoyaltySplitOut, status_code=201)
def add_royalty_split_to_release(
    release_id: int,
    split_data: schemas.RoyaltySplitCreate,
    db: Session = Depends(database.get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    return crud.create_royalty_split_for_release(
        db=db,
        split_data=split_data,
        release_id=release_id,
        owner_id=current_user_id
    )