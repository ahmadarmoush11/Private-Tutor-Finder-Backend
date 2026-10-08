from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.shared.schemas import OptionalText
from app.features.users.schemas import UserSummary


class ClientProfileCreate(BaseModel):
    grade: int | None = Field(default=None, ge=1, le=12)
    school: OptionalText = None
    location: OptionalText = None


class ClientProfileUpdate(BaseModel):
    grade: int | None = Field(default=None, ge=1, le=12)
    school: OptionalText = None
    location: OptionalText = None


class ClientProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    grade: int | None
    school: str | None
    location: str | None
    created_at: datetime
    updated_at: datetime
    user: UserSummary
