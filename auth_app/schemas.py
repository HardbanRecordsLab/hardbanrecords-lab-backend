# auth_app/schemas.py
from pydantic import BaseModel, EmailStr

# --- Schematy Użytkownika (już je miałeś) ---

class UserCreate(BaseModel):
    """Schemat używany do tworzenia nowego użytkownika."""
    email: EmailStr
    password: str

class UserOut(BaseModel):
    """Schemat używany do bezpiecznego zwracania danych użytkownika (bez hasła)."""
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

# --- NOWE Schematy do obsługi Tokenów JWT (logowanie) ---

class Token(BaseModel):
    """Schemat odpowiedzi, gdy użytkownik pomyślnie się zaloguje."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Schemat danych, które będziemy przechowywać wewnątrz tokena JWT."""
    email: EmailStr | None = None