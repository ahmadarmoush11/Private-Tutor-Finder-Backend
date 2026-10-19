from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.features.client_posts.schemas import ClientPostResponse
from app.features.tutor_profiles.schemas import TutorProfileOut


class AvailableTutorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tutor: TutorProfileOut
    created_at: datetime


class TutorAvailabilityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    client_post: ClientPostResponse
    created_at: datetime
