from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.features.class_levels.schemas import ClassLevelOut
from app.features.subjects.schemas import SubjectOut

from app.features.tutor_profiles.model import ExperienceLevel
from app.shared.schemas import OptionalLongText, OptionalText, unique_ids
from app.features.users.schemas import UserSummary


class TutorProfileCreate(BaseModel):
    workplace: OptionalText = None
    degree: OptionalText = None
    summary: OptionalLongText = None
    experience_level: ExperienceLevel
    class_level_ids: list[int] = Field(min_length=1)
    subject_ids: list[int] = Field(min_length=1)

    @field_validator("class_level_ids", "subject_ids")
    @classmethod
    def remove_duplicate_ids(cls, value: list[int]) -> list[int]:
        return unique_ids(value)


class TutorProfileUpdate(BaseModel):
    workplace: OptionalText = None
    degree: OptionalText = None
    summary: OptionalLongText = None
    experience_level: ExperienceLevel | None = None
    class_level_ids: list[int] | None = Field(default=None, min_length=1)
    subject_ids: list[int] | None = Field(default=None, min_length=1)

    @field_validator("experience_level", "class_level_ids", "subject_ids")
    @classmethod
    def not_null(cls, value):
        if value is None:
            raise ValueError("cannot be null")
        return value

    @field_validator("class_level_ids", "subject_ids")
    @classmethod
    def remove_duplicate_ids(cls, value: list[int]) -> list[int]:
        return unique_ids(value)


class TutorProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    workplace: str | None
    degree: str | None
    summary: str | None
    experience_level: ExperienceLevel
    class_levels: list[ClassLevelOut]
    subjects: list[SubjectOut]
    created_at: datetime
    updated_at: datetime
    user: UserSummary


class TutorProfileReviewOut(BaseModel):
    id: int
    reviewer: UserSummary
    rating: int
    comment: str | None
    created_at: datetime
    updated_at: datetime


class TutorProfileDetailOut(TutorProfileOut):
    average_rating: float | None
    review_count: int
    reviews: list[TutorProfileReviewOut]


class TutorSearchParams(BaseModel):
    name: OptionalText = None
    workplace: OptionalText = None
    degree: OptionalText = None
    experience_level: list[ExperienceLevel] | None = None
    subject_id: list[int] | None = None
    class_level_id: list[int] | None = None
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
