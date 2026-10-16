from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator

from app.features.class_levels.schemas import ClassLevelOut
from app.features.users.schemas import UserSummary
from app.shared.enums import Currency, LessonLocation, PostStatus, PriceUnit
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
    budget_min: Decimal = Field(ge=0, max_digits=12, decimal_places=2)
    budget_max: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    currency: Currency
    price_unit: PriceUnit

    @field_validator("subject_ids")
    @classmethod
    def remove_duplicate_ids(cls, value: list[int]) -> list[int]:
        return unique_ids(value)

    @field_validator("budget_max")
    @classmethod
    def budget_max_not_below_min(cls, value: Decimal, info: ValidationInfo) -> Decimal:
        budget_min = info.data.get("budget_min")
        if budget_min is not None and value < budget_min:
            raise ValueError("must be greater than or equal to budget_min")
        return value


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
    budget_min: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)
    budget_max: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=2)
    currency: Currency | None = None
    price_unit: PriceUnit | None = None

    @field_validator(
        "class_level_id",
        "subject_ids",
        "lesson_location",
        "status",
        "address_details",
        "phone_number",
        "description",
        "budget_min",
        "budget_max",
        "currency",
        "price_unit",
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
    budget_min: Decimal | None
    budget_max: Decimal | None
    currency: Currency | None
    price_unit: PriceUnit | None
    created_at: datetime
    updated_at: datetime
