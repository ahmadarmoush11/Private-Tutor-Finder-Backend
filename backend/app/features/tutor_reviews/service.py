from app.core.exceptions import ProfileNotFoundError
from app.db.unit_of_work import UnitOfWork
from app.features.client_profiles.model import ClientProfile
from app.features.client_profiles.repository import ClientProfileRepository
from app.features.tutor_profiles.model import TutorProfile
from app.features.tutor_profiles.repository import TutorProfileRepository
from app.features.tutor_reviews.exceptions import (
    TutorReviewAlreadyExistsError,
    TutorReviewNotFoundError,
)
from app.features.tutor_reviews.model import TutorReview
from app.features.tutor_reviews.repository import TutorReviewRepository
from app.features.tutor_reviews.schemas import TutorReviewCreate, TutorReviewUpdate


class TutorReviewService:
    def __init__(
        self,
        tutor_review_repository: TutorReviewRepository,
        client_profile_repository: ClientProfileRepository,
        tutor_profile_repository: TutorProfileRepository,
        uow: UnitOfWork,
    ):
        self.tutor_review_repository = tutor_review_repository
        self.client_profile_repository = client_profile_repository
        self.tutor_profile_repository = tutor_profile_repository
        self.uow = uow

    def create(self, user_id: int, data: TutorReviewCreate) -> TutorReview:
        client_profile = self._get_client_profile_of_user(user_id)
        tutor_profile = self._get_tutor_profile(data.tutor_user_id)

        if self.tutor_review_repository.get_by_client_and_tutor(
            client_profile.id,
            tutor_profile.id,
        ):
            raise TutorReviewAlreadyExistsError()

        review = TutorReview(
            client_id=client_profile.id,
            tutor_id=tutor_profile.id,
            rating=data.rating,
            comment=data.comment,
        )
        with self.uow:
            review = self.tutor_review_repository.create(review)
        return self.tutor_review_repository.get_by_id(review.id)

    def update(
        self,
        user_id: int,
        tutor_review_id: int,
        data: TutorReviewUpdate,
    ) -> TutorReview:
        client_profile = self._get_client_profile_of_user(user_id)
        review = self._get_tutor_review_of_client(client_profile.id, tutor_review_id)
        values = data.model_dump(exclude_unset=True)

        with self.uow:
            review = self.tutor_review_repository.update(review, values)
        return review

    def delete(self, user_id: int, tutor_review_id: int) -> None:
        client_profile = self._get_client_profile_of_user(user_id)
        review = self._get_tutor_review_of_client(client_profile.id, tutor_review_id)

        with self.uow:
            self.tutor_review_repository.delete(review)

    def get_my_reviews(self, user_id: int) -> list[TutorReview]:
        client_profile = self._get_client_profile_of_user(user_id)
        return self.tutor_review_repository.get_by_client_id(client_profile.id)

    def get_reviews_of_tutor(self, tutor_user_id: int) -> list[TutorReview]:
        self._get_tutor_profile(tutor_user_id)
        return self.tutor_review_repository.get_by_tutor_id(tutor_user_id)

    def get_average_rating_of_tutor(self, tutor_user_id: int) -> float | None:
        tutor_profile = self._get_tutor_profile(tutor_user_id)
        average_rating, _ = self.tutor_review_repository.get_rating_summary(tutor_profile.id)
        return average_rating

    def _get_client_profile_of_user(self, user_id: int) -> ClientProfile:
        client_profile = self.client_profile_repository.get_by_user_id(user_id)
        if client_profile is None:
            raise ProfileNotFoundError("Client profile does not exist")
        return client_profile

    def _get_tutor_profile(self, tutor_user_id: int) -> TutorProfile:
        tutor_profile = self.tutor_profile_repository.get_by_user_id(tutor_user_id)
        if tutor_profile is None:
            raise ProfileNotFoundError("Tutor not found")
        return tutor_profile

    def _get_tutor_review_of_client(
        self,
        client_id: int,
        tutor_review_id: int,
    ) -> TutorReview:
        review = self.tutor_review_repository.get_by_id_for_client(client_id, tutor_review_id)
        if review is None:
            raise TutorReviewNotFoundError()
        return review
