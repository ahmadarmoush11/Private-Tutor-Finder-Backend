from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.features.users.schemas import UserSummary


class ClientProfileCreate(BaseModel):
    pass


class ClientProfileUpdate(BaseModel):
    pass


class ClientProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    user: UserSummary
