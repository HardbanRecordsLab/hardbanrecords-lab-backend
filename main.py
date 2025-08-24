# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importujemy modele i silnik bazy danych
from common import models
from database import engine

# Importujemy routery z naszych modułów
from auth_app import router as auth_router
from music_app import router as music_router

# Tworzymy tabele w bazie danych na podstawie naszych modeli SQLAlchemy.
# Ta linia jest kluczowa - bez niej aplikacja nie będzie wiedziała,
# jakie tabele ma utworzyć przy pierwszym uruchomieniu.
models.Base.metadata.create_all(bind=engine)

# Inicjalizacja głównej aplikacji FastAPI
app = FastAPI(
    title="HardbanRecords Lab API",
    description="Kompleksowa platforma dla niezależnych twórców cyfrowych.",
    version="1.0.0"
)

# Konfiguracja CORS (Cross-Origin Resource Sharing)
# To jest absolutnie kluczowe dla architektury decoupled.
# Pozwala przeglądarce (na której działa frontend) na wysyłanie
# zapytań do naszego serwera backendowego, który działa na innym porcie.
origins = [
    "http://localhost:5173", # Adres serwera deweloperskiego Vite
    "http://localhost:3000", # Popularny adres dla Create React App
    "https://app.hardbanrecords-lab.eu" # Adres produkcyjny
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Pozwalamy na wszystkie metody HTTP (GET, POST, etc.)
    allow_headers=["*"], # Pozwalamy na wszystkie nagłówki
)

# Dołączamy routery z poszczególnych modułów do głównej aplikacji.
# Dzięki temu endpointy z auth_app i music_app będą dostępne w API.
app.include_router(auth_router.router)
app.include_router(music_router.router)

# Główny endpoint powitalny
@app.get("/")
def read_root():
    """
    Główny endpoint API, który zwraca podstawowe informacje
    o statusie i dostępnych usługach.
    """
    return {
        "message": "HardbanRecords Lab API",
        "version": "1.0.0",
        "status": "✅ Running",
        "services": {
            "auth": "/auth/docs",
            "music": "/music/docs",
            "docs": "/docs" # Główna dokumentacja Swagger UI
        }
    }