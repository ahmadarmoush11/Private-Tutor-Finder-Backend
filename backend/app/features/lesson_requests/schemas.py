from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.features.class_levels.schemas import ClassLevelOut
from app.features.client_profiles.schemas import ClientProfileOut
from app.features.subjects.schemas import SubjectOut
from app.features.tutor_profiles.schemas import TutorProfileOut
from app.shared.enums import LessonLocation, RequestStatus
from app.shared.schemas import OptionalLongText, unique_ids


class LessonRequestCreate(BaseModel):
    tutor_user_id: int
    subject_ids: list[int] = Field(min_length=1)
    class_level_id: int
    lesson_location: LessonLocation = LessonLocation.ANY
    message: OptionalLongText = None

    @field_validator("subject_ids")
    @classmethod
    def remove_duplicate_ids(cls, value: list[int]) -> list[int]:
        return unique_ids(value)


class LessonRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    client: ClientProfileOut
    tutor: TutorProfileOut
    subjects: list[SubjectOut]
    class_level: ClassLevelOut
    lesson_location: LessonLocation
    message: str | None
    status: RequestStatus
    created_at: datetime
    updated_at: datetime
