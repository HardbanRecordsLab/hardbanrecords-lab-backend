# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# POPRAWIONY IMPORT: Importujemy 'engine' i 'Base' z nowej, centralnej lokalizacji
from common.database import engine, Base

# POPRAWIONY IMPORT: Importujemy routery z modułów
from auth_app import router as auth_router
from music_app import router as music_router

# Tworzymy wszystkie tabele zdefiniowane w modelach, które dziedziczą z 'Base'.
# To polecenie zostanie wykonane przy starcie aplikacji.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HardbanRecords Lab API",
    description="Kompleksowa platforma dla niezależnych twórców cyfrowych.",
    version="1.0.0"
)

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://app.hardbanrecords-lab.eu"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(music_router.router)

@app.get("/")
def read_root():
    return {
        "message": "HardbanRecords Lab API",
        "version": "1.0.0",
        "status": "✅ Running",
        "services": {
            "auth": "/auth/docs",
            "music": "/music/docs",
            "docs": "/docs"
        }
    }