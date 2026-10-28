from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.features.tutor_profiles.schemas import TutorProfileOut
from app.features.users.schemas import UserSummary
from app.shared.enums import VerificationStatus


class DegreePhotoCreate(BaseModel):
    photo_path: str = Field(min_length=1, max_length=500)


class NationalIdPhotoCreate(BaseModel):
    photo_path: str = Field(min_length=1, max_length=500)


class DegreeVerificationRequestCreate(BaseModel):
    degree: str = Field(min_length=1, max_length=150)
    degree_photos: list[DegreePhotoCreate] = Field(min_length=1)
    national_id_photos: list[NationalIdPhotoCreate] = Field(min_length=1)

    @field_validator("degree")
    @classmethod
    def strip_degree(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be empty")
        return value


class DegreeVerificationReview(BaseModel):
    status: VerificationStatus


class DegreePhotoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    degree_verification_id: int
    photo_path: str
    created_at: datetime


class NationalIdPhotoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    degree_verification_id: int
    photo_path: str
    created_at: datetime


class DegreeVerificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    degree: str
    status: VerificationStatus
    degree_photos: list[DegreePhotoResponse]
    reviewed_at: datetime | None
    created_at: datetime
    updated_at: datetime


class DegreeVerificationAdminResponse(DegreeVerificationResponse):
    tutor_profile: TutorProfileOut
    national_id_photos: list[NationalIdPhotoResponse]
    reviewed_by: UserSummary | None
