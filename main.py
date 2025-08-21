# main.py - GŁÓWNY PLIK APLIKACJI (z diagnostyką)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth_app.main import router as auth_router
from music_app.main import router as music_router
from prometheus_app.main import app as prometheus_app

# Test połączenia z bazą danych przy starcie
print("🚀 Starting HardbanRecords Lab API...")

try:
    from common.database import engine, settings
    # Test połączenia z bazą
    with engine.connect() as connection:
        print("✅ Database connection test successful")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    print("🔧 Check your DATABASE_URL environment variable")

# Główna aplikacja
app = FastAPI(
    title="HardbanRecords Lab API",
    description="Kompleksowa platforma dystrybucji muzyki i książek",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hardbanrecords-lab.eu", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routery
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(music_router, prefix="/music", tags=["Music"])
app.mount("/ai", prometheus_app)

@app.get("/")
def read_root():
    return {
        "message": "HardbanRecords Lab API",
        "version": "1.0.0",
        "status": "✅ Running",
        "services": {
            "auth": "/auth/docs",
            "music": "/music/docs", 
            "ai": "/ai/docs",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health_check():
    try:
        # Test połączenia z bazą
        from common.database import engine
        with engine.connect() as connection:
            db_status = "healthy"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "database": db_status,
        "services": ["auth", "music", "ai"]
    }