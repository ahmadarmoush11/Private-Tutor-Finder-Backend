from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import ProfileAlreadyExistsError
from app.features.tutor_profiles.model import TutorProfile


class TutorProfileRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, profile_id: int) -> TutorProfile | None:
        return self.db.get(TutorProfile, profile_id)

    def get_by_user_id(self, user_id: int) -> TutorProfile | None:
        return self.db.scalar(
            select(TutorProfile).where(TutorProfile.user_id == user_id)
        )

    def create(self, profile: TutorProfile) -> TutorProfile:
        self.db.add(profile)
        try:
            self.db.flush()
        except IntegrityError:
            raise ProfileAlreadyExistsError()
        self.db.refresh(profile)
        return profile

    def update(self, profile: TutorProfile, values: dict) -> TutorProfile:
        for field, value in values.items():
            setattr(profile, field, value)
        self.db.flush()
        self.db.refresh(profile)
        return profile
