from sqlalchemy import exists, func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.core.exceptions import ProfileAlreadyExistsError
from app.features.tutor_profiles.model import (
    ExperienceLevel,
    TutorProfile,
    tutor_profile_class_levels,
    tutor_profile_subjects,
)
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
        name: str | None,
        workplace: str | None,
        degree: str | None,
        experience_levels: list[ExperienceLevel] | None,
        subject_ids: list[int] | None,
        class_level_ids: list[int] | None,
        limit: int,
        offset: int,
    ) -> list[TutorProfile]:
        statement = (
            select(TutorProfile)
            .join(TutorProfile.user)
            .options(selectinload(TutorProfile.user))
        )

        if name:
            for word in name.split():
                statement = statement.where(
                    or_(
                        User.first_name.icontains(word, autoescape=True),
                        User.last_name.icontains(word, autoescape=True),
                        User.username.icontains(word, autoescape=True),
                    )
                )
        if workplace:
            statement = statement.where(TutorProfile.workplace.icontains(workplace, autoescape=True))
        if degree:
            statement = statement.where(TutorProfile.degree.icontains(degree, autoescape=True))
        if experience_levels:
            statement = statement.where(TutorProfile.experience_level.in_(experience_levels))
        if subject_ids:
            statement = statement.where(
                exists().where(
                    tutor_profile_subjects.c.tutor_profile_id == TutorProfile.id,
                    tutor_profile_subjects.c.subject_id.in_(subject_ids),
                )
            )
        if class_level_ids:
            statement = statement.where(
                exists().where(
                    tutor_profile_class_levels.c.tutor_profile_id == TutorProfile.id,
                    tutor_profile_class_levels.c.class_level_id.in_(class_level_ids),
                )
            )

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
