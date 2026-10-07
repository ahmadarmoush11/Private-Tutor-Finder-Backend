from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import ProfileAlreadyExistsError
from app.models.client_profile import ClientProfile


class ClientProfileRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user_id(self, user_id: int) -> ClientProfile | None:
        return self.db.scalar(
            select(ClientProfile).where(ClientProfile.user_id == user_id)
        )

    def create(self, profile: ClientProfile) -> ClientProfile:
        self.db.add(profile)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise ProfileAlreadyExistsError()
        self.db.refresh(profile)
        return profile

    def update(self, profile: ClientProfile, values: dict) -> ClientProfile:
        for field, value in values.items():
            setattr(profile, field, value)
        self.db.commit()
        self.db.refresh(profile)
        return profile
