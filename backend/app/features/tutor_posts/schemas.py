from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.features.class_levels.schemas import ClassLevelOut
from app.shared.enums import LessonLocation, PostStatus
from app.shared.schemas import OptionalText


def _unique_ids(values: list[int]) -> list[int]:
    return list(dict.fromkeys(values))


class TutorPostCreate(BaseModel):
    class_level_ids: list[int] = Field(min_length=1)
    lesson_location: LessonLocation = LessonLocation.ANY
    location: OptionalText = None
    address_details: str = Field(min_length=1, max_length=255)
    phone_number: str = Field(min_length=1, max_length=20)
    description: str = Field(min_length=1)

    @field_validator("class_level_ids")
    @classmethod
    def unique_class_level_ids(cls, value: list[int]) -> list[int]:
        return _unique_ids(value)


class TutorPostUpdate(BaseModel):
    class_level_ids: list[int] | None = Field(default=None, min_length=1)
    lesson_location: LessonLocation | None = None
    status: PostStatus | None = None
    location: OptionalText = None
    address_details: str | None = Field(default=None, min_length=1, max_length=255)
    phone_number: str | None = Field(default=None, min_length=1, max_length=20)
    description: str | None = Field(default=None, min_length=1)

    @field_validator(
        "class_level_ids",
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

    @field_validator("class_level_ids")
    @classmethod
    def unique_class_level_ids(cls, value: list[int]) -> list[int]:
        return _unique_ids(value)


class TutorPostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tutor_id: int
    class_levels: list[ClassLevelOut]
    lesson_location: LessonLocation
    status: PostStatus
    location: str | None
    address_details: str
    phone_number: str
    description: str
    created_at: datetime
    updated_at: datetime
