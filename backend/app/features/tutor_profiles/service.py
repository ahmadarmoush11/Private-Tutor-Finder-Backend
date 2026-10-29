from app.core.exceptions import ProfileAlreadyExistsError, ProfileNotFoundError
from app.features.class_levels.exceptions import ClassLevelNotFoundError
from app.features.class_levels.model import ClassLevel
from app.features.class_levels.repository import ClassLevelRepository
from app.features.subjects.exceptions import SubjectNotFoundError
from app.features.subjects.model import Subject
from app.features.subjects.repository import SubjectRepository
from app.features.areas.exceptions import AreaNotFoundError
from app.features.areas.repository import AreaRepository
from app.db.unit_of_work import UnitOfWork
from app.features.tutor_profiles.model import TutorProfile
from app.features.tutor_reviews.repository import TutorReviewRepository
from app.features.users.model import User
from app.features.tutor_profiles.repository import TutorProfileRepository
from app.features.tutor_profiles.schemas import (
    TutorProfileCreate,
    TutorProfileDetailOut,
    TutorProfileOut,
    TutorProfileReviewOut,
    TutorProfileUpdate,
    TutorSearchParams,
)


class TutorProfileService:
    def __init__(
        self,
        tutor_profile_repository: TutorProfileRepository,
        class_level_repository: ClassLevelRepository,
        subject_repository: SubjectRepository,
        tutor_review_repository: TutorReviewRepository,
        area_repository: AreaRepository,
        uow: UnitOfWork,
    ):
        self.tutor_profile_repository = tutor_profile_repository
        self.class_level_repository = class_level_repository
        self.subject_repository = subject_repository
        self.tutor_review_repository = tutor_review_repository
        self.area_repository = area_repository
        self.uow = uow

    def get_by_user_id(self, user_id: int) -> TutorProfile:
        profile = self.tutor_profile_repository.get_by_user_id(user_id)
        if profile is None:
            raise ProfileNotFoundError("Tutor profile not found")
        return profile

    def get_profile_details(self, user_id: int) -> TutorProfileDetailOut:
        profile = self.get_by_user_id(user_id)
        average_rating, review_count = self.tutor_review_repository.get_rating_summary(
            profile.id
        )
        reviews = self.tutor_review_repository.get_by_tutor_id(user_id)

        return TutorProfileDetailOut(
            **TutorProfileOut.model_validate(profile).model_dump(),
            average_rating=average_rating,
            review_count=review_count,
            reviews=[
                TutorProfileReviewOut(
                    id=review.id,
                    reviewer=review.client.user,
                    rating=review.rating,
                    comment=review.comment,
                    created_at=review.created_at,
                    updated_at=review.updated_at,
                )
                for review in reviews
            ],
        )

    def create(self, user: User, data: TutorProfileCreate) -> TutorProfile:
        if self.tutor_profile_repository.get_by_user_id(user.id):
            raise ProfileAlreadyExistsError()
        self._ensure_area_exists(data.area_id)
        profile = TutorProfile(
            user_id=user.id,
            class_levels=self._get_class_levels(data.class_level_ids),
            subjects=self._get_subjects(data.subject_ids),
            **data.model_dump(exclude={"class_level_ids", "subject_ids"}),
        )
        with self.uow:
            profile = self.tutor_profile_repository.create(profile)
        return profile

    def update(self, user: User, data: TutorProfileUpdate) -> TutorProfile:
        profile = self.get_by_user_id(user.id)
        values = data.model_dump(exclude_unset=True)

        if "area_id" in values:
            self._ensure_area_exists(values["area_id"])

        if "class_level_ids" in values:
            values["class_levels"] = self._get_class_levels(values.pop("class_level_ids"))
        if "subject_ids" in values:
            values["subjects"] = self._get_subjects(values.pop("subject_ids"))

        with self.uow:
            profile = self.tutor_profile_repository.update(profile, values)
        return profile

    def search(self, params: TutorSearchParams) -> list[TutorProfile]:
        return self.tutor_profile_repository.search(
            name=params.name,
            workplace=params.workplace,
            degree=params.degree,
            experience_levels=params.experience_level,
            subject_ids=params.subject_id,
            class_level_ids=params.class_level_id,
            limit=params.limit,
            offset=params.offset,
        )

    def _get_class_levels(self, class_level_ids: list[int]) -> list[ClassLevel]:
        class_levels = self.class_level_repository.get_by_ids(class_level_ids)
        found_ids = {class_level.id for class_level in class_levels}
        missing_ids = [
            class_level_id
            for class_level_id in class_level_ids
            if class_level_id not in found_ids
        ]
        if missing_ids:
            raise ClassLevelNotFoundError(details={"missing_ids": missing_ids})
        return class_levels

    def _get_subjects(self, subject_ids: list[int]) -> list[Subject]:
        subjects = self.subject_repository.get_by_ids(subject_ids)
        found_ids = {subject.id for subject in subjects}
        missing_ids = [
            subject_id for subject_id in subject_ids if subject_id not in found_ids
        ]
        if missing_ids:
            raise SubjectNotFoundError(details={"missing_ids": missing_ids})
        return subjects

    def _ensure_area_exists(self, area_id: int) -> None:
        if self.area_repository.get_by_id(area_id) is None:
            raise AreaNotFoundError()
