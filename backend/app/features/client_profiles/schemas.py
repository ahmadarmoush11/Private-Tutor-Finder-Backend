from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, field_validator

from app.features.users.schemas import UserSummary
from app.shared.dates import validate_date_of_birth


class ClientProfileCreate(BaseModel):
    date_of_birth: date

    @field_validator("date_of_birth")
    @classmethod
    def realistic_date_of_birth(cls, value: date) -> date:
        return validate_date_of_birth(value)


class ClientProfileUpdate(BaseModel):
    date_of_birth: date | None = None

    @field_validator("date_of_birth")
    @classmethod
    def realistic_date_of_birth(cls, value: date | None) -> date:
        if value is None:
            raise ValueError("cannot be null")
        return validate_date_of_birth(value)


class ClientProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    user: UserSummary
