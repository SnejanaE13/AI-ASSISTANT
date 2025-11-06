from pydantic import BaseModel, EmailStr, constr, field_validator
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    student = "student"
    teacher = "teacher"

class UserCreate(BaseModel):
    email: EmailStr
    # Пароль должен быть >= 9 символов, как в script.js
    password: constr(min_length=9)
    first_name: str
    last_name: str
    second_name: Optional[str] = None
    role: UserRole

    @field_validator("password")
    @classmethod
    def password_must_be_within_72_bytes(cls, v: str) -> str:
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Пароль не может превышать 72 байта (проблема с кириллицей).")
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    session_token: str
    user_role: str


class UserResponse(BaseModel):
    user_id: int
    email: EmailStr
    role: str
    first_name: str

    class Config:
        from_attributes = True

class ChatMessage(BaseModel):
    content: constr(max_length=500)  # Лимит 500 символов из тз

class MessageCreate(BaseModel):
    user_id: int
    session_id: str
    sender_type: str
    content: str
