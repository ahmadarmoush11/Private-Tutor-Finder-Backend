from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.features.client_profiles.model import ClientProfile
from app.features.tutor_profiles.model import TutorProfile
from app.features.tutor_reviews.exceptions import TutorReviewAlreadyExistsError
from app.features.tutor_reviews.model import TutorReview


def _load_details():
    return (
        selectinload(TutorReview.client).selectinload(ClientProfile.user),
        selectinload(TutorReview.tutor).selectinload(TutorProfile.user),
    )


class TutorReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, tutor_review: TutorReview) -> TutorReview:
        self.db.add(tutor_review)
        try:
            self.db.flush()
        except IntegrityError:
            raise TutorReviewAlreadyExistsError()
        self.db.refresh(tutor_review)
        return tutor_review

    def get_by_id(self, tutor_review_id: int) -> TutorReview | None:
        return self.db.scalar(
            select(TutorReview)
            .options(*_load_details())
            .where(TutorReview.id == tutor_review_id)
        )

    def get_by_client_and_tutor(
        self,
        client_id: int,
        tutor_id: int,
    ) -> TutorReview | None:
        return self.db.scalar(
            select(TutorReview).where(
                TutorReview.client_id == client_id,
                TutorReview.tutor_id == tutor_id,
            )
        )

    def get_by_id_for_client(
        self,
        client_id: int,
        tutor_review_id: int,
    ) -> TutorReview | None:
        return self.db.scalar(
            select(TutorReview)
            .options(*_load_details())
            .where(
                TutorReview.id == tutor_review_id,
                TutorReview.client_id == client_id,
            )
        )

    def get_by_tutor_id(self, tutor_user_id: int) -> list[TutorReview]:
        return list(
            self.db.scalars(
                select(TutorReview)
                .join(TutorReview.tutor)
                .options(*_load_details())
                .where(TutorProfile.user_id == tutor_user_id)
                .order_by(TutorReview.created_at.desc(), TutorReview.id.desc())
            )
        )

    def get_by_client_id(self, client_id: int) -> list[TutorReview]:
        return list(
            self.db.scalars(
                select(TutorReview)
                .options(*_load_details())
                .where(TutorReview.client_id == client_id)
                .order_by(TutorReview.created_at.desc(), TutorReview.id.desc())
            )
        )

    def get_rating_summary(self, tutor_profile_id: int) -> tuple[float | None, int]:
        average, count = self.db.execute(
            select(func.avg(TutorReview.rating), func.count(TutorReview.id))
            .where(TutorReview.tutor_id == tutor_profile_id)
        ).one()
        if average is None:
            return None, 0
        return round(float(average), 1), count

    def update(self, tutor_review: TutorReview, values: dict) -> TutorReview:
        for field, value in values.items():
            setattr(tutor_review, field, value)
        self.db.flush()
        self.db.refresh(tutor_review)
        return tutor_review

    def delete(self, tutor_review: TutorReview) -> None:
        self.db.delete(tutor_review)
        self.db.flush()
