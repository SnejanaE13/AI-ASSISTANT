from pydantic import BaseModel, EmailStr, constr, field_validator
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    # Пароль должен быть >= 8 символов, как в script.js
    password: constr(min_length=8)
    first_name: str
    last_name: str
    second_name: Optional[str] = None
    role: str  # 'student' или 'teacher'

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
