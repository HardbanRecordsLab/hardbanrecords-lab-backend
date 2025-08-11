# common/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    sqlalchemy_database_url: str = "postgresql://user:password@postgresserver/db"
    class Config:
        env_file = ".env"

settings = Settings()
engine = create_engine(settings.sqlalchemy_database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()