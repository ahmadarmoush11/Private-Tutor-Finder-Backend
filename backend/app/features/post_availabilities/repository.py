from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.features.client_posts.model import ClientPost
from app.features.client_profiles.model import ClientProfile
from app.features.post_availabilities.exceptions import AlreadyAvailableError
from app.features.post_availabilities.model import PostAvailability
from app.features.tutor_profiles.model import TutorProfile


class PostAvailabilityRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, availability: PostAvailability) -> PostAvailability:
        self.db.add(availability)
        try:
            self.db.flush()
        except IntegrityError:
            raise AlreadyAvailableError()
        self.db.refresh(availability)
        return availability

    def get(self, tutor_profile_id: int, client_post_id: int) -> PostAvailability | None:
        return self.db.scalar(
            select(PostAvailability)
            .options(*self._load_post())
            .where(
                PostAvailability.tutor_id == tutor_profile_id,
                PostAvailability.client_post_id == client_post_id,
            )
        )

    def get_all_for_post(self, client_post_id: int) -> list[PostAvailability]:
        return list(
            self.db.scalars(
                select(PostAvailability)
                .options(selectinload(PostAvailability.tutor).selectinload(TutorProfile.user))
                .where(PostAvailability.client_post_id == client_post_id)
                .order_by(PostAvailability.created_at, PostAvailability.id)
            )
        )

    def get_all_for_tutor(self, tutor_profile_id: int) -> list[PostAvailability]:
        return list(
            self.db.scalars(
                select(PostAvailability)
                .options(*self._load_post())
                .where(PostAvailability.tutor_id == tutor_profile_id)
                .order_by(PostAvailability.created_at.desc(), PostAvailability.id.desc())
            )
        )

    def delete(self, availability: PostAvailability) -> None:
        self.db.delete(availability)
        self.db.flush()

    @staticmethod
    def _load_post():
        return (
            selectinload(PostAvailability.client_post).selectinload(ClientPost.class_level),
            selectinload(PostAvailability.client_post).selectinload(ClientPost.subjects),
            selectinload(PostAvailability.client_post)
            .selectinload(ClientPost.client)
            .selectinload(ClientProfile.user),
        )
