from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.core.exceptions import ProfileAlreadyExistsError
from app.features.tutor_profiles.model import ExperienceLevel, TutorProfile
from app.features.users.model import User


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

    def search(
        self,
        *,
        first_name: str | None,
        last_name: str | None,
        workplace: str | None,
        degree: str | None,
        experience_levels: list[ExperienceLevel] | None,
        limit: int,
        offset: int,
    ) -> list[TutorProfile]:
        statement = (
            select(TutorProfile)
            .join(TutorProfile.user)
            .options(selectinload(TutorProfile.user))
        )

        if first_name:
            statement = statement.where(User.first_name.icontains(first_name, autoescape=True))
        if last_name:
            statement = statement.where(User.last_name.icontains(last_name, autoescape=True))
        if workplace:
            statement = statement.where(TutorProfile.workplace.icontains(workplace, autoescape=True))
        if degree:
            statement = statement.where(TutorProfile.degree.icontains(degree, autoescape=True))
        if experience_levels:
            statement = statement.where(TutorProfile.experience_level.in_(experience_levels))

        statement = (
            statement.order_by(
                func.lower(User.last_name),
                func.lower(User.first_name),
                TutorProfile.id,
            )
            .limit(limit)
            .offset(offset)
        )
        return list(self.db.scalars(statement))
