from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import ProfileAlreadyExistsError
from app.features.client_profiles.model import ClientProfile


class ClientProfileRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user_id(self, user_id: int) -> ClientProfile | None:
        return self.db.scalar(
            select(ClientProfile).where(ClientProfile.user_id == user_id)
        )


    def get_client_profile(
        self,
        client_id: int,
    ):
        return (
            self.db.query(ClientProfile)
            .filter(ClientProfile.id==client_id)
            .first()
        )


    def create(self, profile: ClientProfile) -> ClientProfile:
        self.db.add(profile)
        try:
            self.db.flush()
        except IntegrityError:
            raise ProfileAlreadyExistsError()
        self.db.refresh(profile)
        return profile

    def update(self, profile: ClientProfile, values: dict) -> ClientProfile:
        for field, value in values.items():
            setattr(profile, field, value)
        self.db.flush()
        self.db.refresh(profile)
        return profile
