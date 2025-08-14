# music_app/schemas.py
from pydantic import BaseModel
from typing import Optional, Dict, Any

# \--- Schemat Podstawowy ---

# Zawiera pola wspólne dla tworzenia i odczytu.

class MusicReleaseBase(BaseModel):
title: str
artist: str
status: Optional[str] = "draft"
metadata: Optional[Dict[str, Any]] = None

# \--- Schemat do Tworzenia ---

# Dziedziczy po MusicReleaseBase, bo potrzebujemy tych samych pól.

class MusicReleaseCreate(MusicReleaseBase):
pass

# \--- Schemat do Odczytu ---

# Ten schemat będzie używany, gdy będziemy zwracać dane z API.

# Zawiera dodatkowo 'id' i 'owner\_id', które są generowane przez bazę danych.

class MusicRelease(MusicReleaseBase):
id: int
owner\_id: int