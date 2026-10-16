from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.features.class_levels.schemas import ClassLevelOut
from app.features.users.schemas import UserSummary
from app.shared.enums import Currency, LessonLocation, PostStatus, PriceUnit
from app.features.subjects.schemas import SubjectOut
from app.shared.schemas import OptionalText, unique_ids


class TutorPostCreate(BaseModel):
    class_level_ids: list[int] = Field(min_length=1)
    subject_ids: list[int] = Field(min_length=1)
    lesson_location: LessonLocation = LessonLocation.ANY
    location: OptionalText = None
    address_details: str = Field(min_length=1, max_length=255)
    phone_number: str = Field(min_length=1, max_length=20)
    description: str = Field(min_length=1)
    price: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    currency: Currency
    price_unit: PriceUnit

    @field_validator("class_level_ids", "subject_ids")
    @classmethod
    def remove_duplicate_ids(cls, value: list[int]) -> list[int]:
        return unique_ids(value)


class TutorPostUpdate(BaseModel):
    class_level_ids: list[int] | None = Field(default=None, min_length=1)
    subject_ids: list[int] | None = Field(default=None, min_length=1)
    lesson_location: LessonLocation | None = None
    status: PostStatus | None = None
    location: OptionalText = None
    address_details: str | None = Field(default=None, min_length=1, max_length=255)
    phone_number: str | None = Field(default=None, min_length=1, max_length=20)
    description: str | None = Field(default=None, min_length=1)
    price: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=2)
    currency: Currency | None = None
    price_unit: PriceUnit | None = None

    @field_validator(
        "class_level_ids",
        "subject_ids",
        "lesson_location",
        "status",
        "address_details",
        "phone_number",
        "description",
        "price",
        "currency",
        "price_unit",
    )
    @classmethod
    def not_null(cls, value):
        if value is None:
            raise ValueError("cannot be null")
        return value

    @field_validator("class_level_ids", "subject_ids")
    @classmethod
    def remove_duplicate_ids(cls, value: list[int]) -> list[int]:
        return unique_ids(value)


class TutorPostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author: UserSummary
    class_levels: list[ClassLevelOut]
    subjects: list[SubjectOut]
    lesson_location: LessonLocation
    status: PostStatus
    location: str | None
    address_details: str
    phone_number: str
    description: str
    price: Decimal | None
    currency: Currency | None
    price_unit: PriceUnit | None
    created_at: datetime
    updated_at: datetime
