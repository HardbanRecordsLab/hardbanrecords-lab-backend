# main.py - GŁÓWNY PLIK APLIKACJI
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
allow_origins=["https://hardbanrecords-lab.eu", "http://localhost:3000"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)
# Dołącz routery z różnych serwisów
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(music_router, prefix="/music", tags=["Music"])
# Mount AI service
app.mount("/ai", prometheus_app)
@app.get("/")
def read_root():
return {
"message": "HardbanRecords Lab API",
"version": "1.0.0",
"services": {
"auth": "/auth",
"music": "/music",
"ai": "/ai",
"docs": "/docs"
KROK 3: Uaktualnij music_app/main.py
GDZIE: Nadpisz plik music_app/main.py
}
}
@app.get("/health")
def health_check():
return {"status": "healthy", "services": ["auth", "music", "ai"]}
