from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

from app.models.tutor_profile import ExperienceLevel
from app.schemas.common import OptionalText
from app.schemas.user import UserSummary


class TutorProfileCreate(BaseModel):
    workplace: OptionalText = None
    degree: OptionalText = None
    experience_level: ExperienceLevel


class TutorProfileUpdate(BaseModel):
    workplace: OptionalText = None
    degree: OptionalText = None
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
    experience_level: ExperienceLevel
    created_at: datetime
    updated_at: datetime
    user: UserSummary
