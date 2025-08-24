# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Wczytuje zmienne z pliku .env na samym początku
load_dotenv()

# Test połączenia z bazą danych przy starcie
print("🚀 Starting HardbanRecords Lab API...")

try:
    from common.database import engine, settings
    with engine.connect() as connection:
        print("✅ Database connection test successful")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    print("🔧 Check your DATABASE_URL environment variable")

# Security check
def security_check():
    issues = []
    if not os.getenv('SECRET_KEY') or len(os.getenv('SECRET_KEY', '')) < 32:
        issues.append("SECRET_KEY is too short or missing")
    if not os.getenv('DATABASE_URL'):
        issues.append("DATABASE_URL is not configured")
    if issues:
        print("🔒 SECURITY WARNINGS:")
        for issue in issues:
            print(f"   ⚠️  {issue}")
    else:
        print("✅ Security check passed")

security_check()

# Import routerów
from auth_app.main import router as auth_router
from music_app.router import router as music_router
from prometheus_app.main import app as prometheus_app

# Główna aplikacja
app = FastAPI(
    title="HardbanRecords Lab API",
    description="Kompleksowa platforma dystrybucji muzyki i książek",
    version="1.0.0"
)

# CORS
origins = [
    "https://hardbanrecordslab2.onrender.com",
    "http://localhost:5173",
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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

@app.get("/security-status")
def security_status():
    return {
        "secret_key_configured": bool(os.getenv('SECRET_KEY')),
        "secret_key_length": len(os.getenv('SECRET_KEY', '')),
        "database_configured": bool(os.getenv('DATABASE_URL')),
        "ai_configured": bool(os.getenv('GROQ_API_KEY')),
        "environment": os.getenv('ENVIRONMENT', 'development')
    }