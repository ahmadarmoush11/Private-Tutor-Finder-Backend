from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.shared.schemas import OptionalText
from app.features.client_posts.model import LessonLocation, PostStatus

class ClientPostCreate(BaseModel):
    class_level_id: int
    school_name: str|None
    lesson_location: LessonLocation = LessonLocation.ANY
    location: str|None
    address_details: str
    phone_number: str
    description: str


class ClientPostUpdate(BaseModel):
    class_level_id: int | None = None
    school_name: OptionalText = None
    lesson_location: LessonLocation | None = None
    status: PostStatus | None = None
    location: OptionalText = None
    address_details: str | None = Field(default=None, min_length=1, max_length=255)
    phone_number: str | None = Field(default=None, min_length=1, max_length=20)
    description: str | None = Field(default=None, min_length=1)

    @field_validator(
        "class_level_id",
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


class ClientPostResponse(BaseModel):
    post_id: int
    client_id: int
    class_level_id: int
    school_name: str|None
    lesson_location: LessonLocation
    status: PostStatus
    location: str|None
    address_details: str
    phone_number: str
    description: str

