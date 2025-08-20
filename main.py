# main.py - GŁÓWNY PLIK APLIKACJI (POPRAWIONY)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth_app.main import router as auth_router
from music_app.main import router as music_router
from prometheus_app.main import app as prometheus_app

# Główna aplikacja
app = FastAPI(
    title="HardbanRecords Lab API",
    description="Kompleksowa platforma dystrybucji muzyki i książek",
    version="1.0.0"
)

# CORS - pozwala na komunikację z frontendem WordPress
app.add_middleware(
    CORSMiddleware,
    # Ustaw tutaj domenę swojego WordPressa, gdy będzie gotowy
    allow_origins=["https://hardbanrecords-lab.eu", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dołącz routery z różnych serwisów
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(music_router, prefix="/music", tags=["Music"])

# Podłącz serwis AI jako pod-aplikację
app.mount("/ai", prometheus_app)

@app.get("/")
def read_root():
    # POPRAWKA: Dodano wcięcie i usunięto zbędny tekst
    return {
        "message": "HardbanRecords Lab API",
        "version": "1.0.0",
        "services": {
            "auth": "/auth/docs",
            "music": "/music/docs",
            "ai": "/ai/docs",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "services": ["auth", "music", "ai"]}