# common/models.py

from sqlalchemy import Column, Integer, String, DateTime, func
# POPRAWIONY IMPORT: Importujemy 'Base' z naszego nowego pliku database.py
from .database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"