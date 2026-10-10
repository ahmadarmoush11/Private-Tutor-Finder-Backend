from app.core.exceptions import (
    ClassLevelNotFoundError,
    PostAccessDeniedError,
    PostNotFoundError,
    ProfileNotFoundError,
)
from app.db.unit_of_work import UnitOfWork
from app.features.class_levels.model import ClassLevel
from app.features.class_levels.repository import ClassLevelRepository
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
        uow: UnitOfWork,
    ):
        self.tutor_post_repository = tutor_post_repository
        self.tutor_profile_repository = tutor_profile_repository
        self.class_level_repository = class_level_repository
        self.uow = uow

    def create(self, user_id: int, data: TutorPostCreate) -> TutorPost:
        tutor_profile = self._get_tutor_profile_of_user(user_id)
        class_levels = self._get_class_levels(data.class_level_ids)

        post = TutorPost(
            tutor_id=tutor_profile.id,
            class_levels=class_levels,
            **data.model_dump(exclude={"class_level_ids"}),
        )

        with self.uow:
            post = self.tutor_post_repository.create(post)
        return post

    def get_post(self, post_id: int) -> TutorPost:
        post = self.tutor_post_repository.get_by_id(post_id)
        if post is None:
            raise PostNotFoundError()
        return post

    def get_tutor_posts(self, tutor_id: int) -> list[TutorPost]:
        if self.tutor_profile_repository.get_by_id(tutor_id) is None:
            raise ProfileNotFoundError("Tutor profile not found")
        return self.tutor_post_repository.get_by_tutor_id(tutor_id)

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
