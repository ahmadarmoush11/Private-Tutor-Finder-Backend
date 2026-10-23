from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from app.features.client_posts.schemas import ClientPostResponse
from app.features.lesson_requests.schemas import LessonRequestResponse
from app.features.users.schemas import UserSummary


class NotificationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    actor: UserSummary | None
    is_read: bool
    created_at: datetime


class LessonRequestReceivedResponse(NotificationBase):
    type: Literal["lesson_request_received"]
    lesson_request: LessonRequestResponse


class LessonRequestAcceptedResponse(NotificationBase):
    type: Literal["lesson_request_accepted"]
    lesson_request: LessonRequestResponse


class LessonRequestRejectedResponse(NotificationBase):
    type: Literal["lesson_request_rejected"]
    lesson_request: LessonRequestResponse


class TutorAvailableResponse(NotificationBase):
    type: Literal["tutor_available"]
    client_post: ClientPostResponse


NotificationResponse = Annotated[
    LessonRequestReceivedResponse
    | LessonRequestAcceptedResponse
    | LessonRequestRejectedResponse
    | TutorAvailableResponse,
    Field(discriminator="type"),
]