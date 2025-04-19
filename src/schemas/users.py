from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class User(BaseModel):
    id: int
    created_at: str
    username: str
    email: Optional[EmailStr] = None


class UserDB(User):
    password: str


class UserCreate(BaseModel):
    """Esquema para la creación de un usuario."""
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """Esquema para actualizar datos del usuario."""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=100)