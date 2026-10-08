from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

from app.features.tutor_profiles.model import ExperienceLevel
from app.shared.schemas import OptionalLongText, OptionalText
from app.features.users.schemas import UserSummary


class TutorProfileCreate(BaseModel):
    workplace: OptionalText = None
    degree: OptionalText = None
    summary: OptionalLongText = None
    experience_level: ExperienceLevel


class TutorProfileUpdate(BaseModel):
    workplace: OptionalText = None
    degree: OptionalText = None
    summary: OptionalLongText = None
    experience_level: ExperienceLevel | None = None

    @field_validator("experience_level")
    @classmethod
    def experience_level_not_null(cls, value: ExperienceLevel | None) -> ExperienceLevel:
        if value is None:
            raise ValueError("cannot be null")
        return value


class TutorProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    workplace: str | None
    degree: str | None
    summary: str | None
    experience_level: ExperienceLevel
    created_at: datetime
    updated_at: datetime
    user: UserSummary
