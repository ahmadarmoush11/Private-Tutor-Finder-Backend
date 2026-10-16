from app.core.exceptions import (
    PostAccessDeniedError,
    PostNotFoundError,
    ProfileNotFoundError,
    ViewAccessDeniedError,
)
from app.features.class_levels.exceptions import ClassLevelNotFoundError
from app.features.subjects.exceptions import SubjectNotFoundError
from app.db.unit_of_work import UnitOfWork
from app.features.users.model import User, UserRole
from app.features.class_levels.model import ClassLevel
from app.features.class_levels.repository import ClassLevelRepository
from app.features.subjects.model import Subject
from app.features.subjects.repository import SubjectRepository
from app.features.tutor_posts.model import TutorPost
from app.features.tutor_posts.repository import TutorPostRepository
from app.features.tutor_posts.schemas import TutorPostCreate, TutorPostUpdate
from app.features.tutor_profiles.model import TutorProfile
from app.features.tutor_profiles.repository import TutorProfileRepository


class TutorPostService:
    def __init__(
        self,
        tutor_post_repository: TutorPostRepository,
        tutor_profile_repository: TutorProfileRepository,
        class_level_repository: ClassLevelRepository,
        subject_repository: SubjectRepository,
        uow: UnitOfWork,
    ):
        self.tutor_post_repository = tutor_post_repository
        self.tutor_profile_repository = tutor_profile_repository
        self.class_level_repository = class_level_repository
        self.subject_repository = subject_repository
        self.uow = uow

    def create(self, user_id: int, data: TutorPostCreate) -> TutorPost:
        tutor_profile = self._get_tutor_profile_of_user(user_id)
        class_levels = self._get_class_levels(data.class_level_ids)
        subjects = self._get_subjects(data.subject_ids)

        post = TutorPost(
            tutor_id=tutor_profile.id,
            class_levels=class_levels,
            subjects=subjects,
            **data.model_dump(exclude={"class_level_ids", "subject_ids"}),
        )

        with self.uow:
            post = self.tutor_post_repository.create(post)
        return post

    def get_post_for_viewer(self, post_id: int, viewer: User) -> TutorPost:
        post = self.get_post(post_id)
        self._ensure_can_view(viewer, post.tutor.user_id)
        return post

    def get_post(self, post_id: int) -> TutorPost:
        post = self.tutor_post_repository.get_by_id(post_id)
        if post is None:
            raise PostNotFoundError()
        return post

    def get_tutor_posts(self, user_id: int, viewer: User) -> list[TutorPost]:
        self._ensure_can_view(viewer, user_id)
        tutor_profile = self.tutor_profile_repository.get_by_user_id(user_id)
        if tutor_profile is None:
            raise ProfileNotFoundError("Tutor profile not found")
        return self.tutor_post_repository.get_by_tutor_id(tutor_profile.id)

    def get_my_posts(self, user_id: int) -> list[TutorPost]:
        tutor_profile = self._get_tutor_profile_of_user(user_id)
        return self.tutor_post_repository.get_by_tutor_id(tutor_profile.id)

    def update_post(
        self,
        user_id: int,
        post_id: int,
        data: TutorPostUpdate,
    ) -> TutorPost:
        post = self._get_own_post(user_id, post_id)
        values = data.model_dump(exclude_unset=True)

        if "class_level_ids" in values:
            values["class_levels"] = self._get_class_levels(
                values.pop("class_level_ids")
            )

        if "subject_ids" in values:
            values["subjects"] = self._get_subjects(values.pop("subject_ids"))

        with self.uow:
            post = self.tutor_post_repository.update(post, values)
        return post

    def delete_post(self, user_id: int, post_id: int) -> None:
        post = self._get_own_post(user_id, post_id)

        with self.uow:
            self.tutor_post_repository.delete(post)

    def _get_tutor_profile_of_user(self, user_id: int) -> TutorProfile:
        tutor_profile = self.tutor_profile_repository.get_by_user_id(user_id)
        if tutor_profile is None:
            raise ProfileNotFoundError("Tutor profile does not exist")
        return tutor_profile

    def _get_own_post(self, user_id: int, post_id: int) -> TutorPost:
        tutor_profile = self._get_tutor_profile_of_user(user_id)
        post = self.get_post(post_id)
        if post.tutor_id != tutor_profile.id:
            raise PostAccessDeniedError()
        return post

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

    @staticmethod
    def _ensure_can_view(viewer: User, owner_user_id: int) -> None:
        if viewer.role == UserRole.TUTOR and viewer.id != owner_user_id:
            raise ViewAccessDeniedError("Tutors can only view their own posts")
