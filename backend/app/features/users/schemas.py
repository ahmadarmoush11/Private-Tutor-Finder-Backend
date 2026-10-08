from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.features.users.model import UserRole


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str | None
    role: UserRole
    has_profile: bool
    created_at: datetime


class UserSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
