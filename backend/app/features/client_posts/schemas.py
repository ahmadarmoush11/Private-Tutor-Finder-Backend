from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.features.class_levels.schemas import ClassLevelOut
from app.features.users.schemas import UserSummary
from app.shared.enums import LessonLocation, PostStatus
from app.features.subjects.schemas import SubjectOut
from app.shared.schemas import OptionalText, unique_ids


class ClientPostCreate(BaseModel):
    class_level_id: int
    subject_ids: list[int] = Field(min_length=1)
    school_name: OptionalText = None
    lesson_location: LessonLocation = LessonLocation.ANY
    location: OptionalText = None
    address_details: str = Field(min_length=1, max_length=255)
    phone_number: str = Field(min_length=1, max_length=20)
    description: str = Field(min_length=1)

    @field_validator("subject_ids")
    @classmethod
    def remove_duplicate_ids(cls, value: list[int]) -> list[int]:
        return unique_ids(value)


class ClientPostUpdate(BaseModel):
    class_level_id: int | None = None
    subject_ids: list[int] | None = Field(default=None, min_length=1)
    school_name: OptionalText = None
    lesson_location: LessonLocation | None = None
    status: PostStatus | None = None
    location: OptionalText = None
    address_details: str | None = Field(default=None, min_length=1, max_length=255)
    phone_number: str | None = Field(default=None, min_length=1, max_length=20)
    description: str | None = Field(default=None, min_length=1)

    @field_validator(
        "class_level_id",
        "subject_ids",
        "lesson_location",
        "status",
        "address_details",
        "phone_number",
        "description",
    )
    @classmethod
    def not_null(cls, value):
        if value is None:
            raise ValueError("cannot be null")
        return value

    @field_validator("subject_ids")
    @classmethod
    def remove_duplicate_ids(cls, value: list[int]) -> list[int]:
        return unique_ids(value)


class ClientPostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author: UserSummary
    class_level_id: int
    class_level: ClassLevelOut
    subjects: list[SubjectOut]
    school_name: str | None
    lesson_location: LessonLocation
    status: PostStatus
    location: str | None
    address_details: str
    phone_number: str
    description: str
    created_at: datetime
    updated_at: datetime
