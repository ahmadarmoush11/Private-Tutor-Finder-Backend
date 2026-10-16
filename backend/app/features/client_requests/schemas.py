from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.features.client_profiles.schemas import ClientProfileOut
from app.features.client_requests.model import RequestStatus
from app.features.tutor_posts.schemas import TutorPostResponse


class ClientRequestCreate(BaseModel):
    tutor_post_id: int


class ClientRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    client: ClientProfileOut
    tutor_post: TutorPostResponse
    status: RequestStatus
    created_at: datetime
    updated_at: datetime

