from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.features.client_profiles.schemas import ClientProfileOut
from app.features.tutor_profiles.schemas import TutorProfileOut
from app.shared.schemas import OptionalLongText


class TutorReviewCreate(BaseModel):
    tutor_user_id: int
    rating: int = Field(ge=1, le=5)
    comment: OptionalLongText = None


class TutorReviewUpdate(BaseModel):
    rating: int | None = Field(default=None, ge=1, le=5)
    comment: OptionalLongText = None

    @field_validator("rating")
    @classmethod
    def rating_not_null(cls, value: int | None) -> int:
        if value is None:
            raise ValueError("cannot be null")
        return value


class TutorReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    client: ClientProfileOut
    tutor: TutorProfileOut
    rating: int
    comment: str | None
    created_at: datetime
    updated_at: datetime
