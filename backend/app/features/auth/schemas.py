from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.features.users.schemas import UserOut


class UserRegister(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    phone_number: str | None = Field(default=None, max_length=20)
    role: Literal["client", "tutor"] = "client"

    @field_validator("first_name", "last_name")
    @classmethod
    def strip_names(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be empty")
        return value

    @field_validator("email")
    @classmethod
    def lowercase_email(cls, value: str) -> str:
        return value.lower()

    @field_validator("password")
    @classmethod
    def password_byte_length(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("password is too long")
        return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AuthResponse(Token):
    user: UserOut
