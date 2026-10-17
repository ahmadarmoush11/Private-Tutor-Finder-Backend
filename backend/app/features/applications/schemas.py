from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.features.client_posts.schemas import ClientPostResponse
from app.features.tutor_profiles.schemas import TutorProfileOut
from app.shared.enums import RequestStatus


class ApplicationCreate(BaseModel):
    client_post_id: int


class ApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tutor: TutorProfileOut
    client_post: ClientPostResponse
    status: RequestStatus
    created_at: datetime
    updated_at: datetime
