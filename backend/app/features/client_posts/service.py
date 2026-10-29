from decimal import Decimal

from app.core.exceptions import (
    PostAccessDeniedError,
    PostNotFoundError,
    ProfileNotFoundError,
    ValidationException,
    ViewAccessDeniedError,
)
from app.features.class_levels.exceptions import ClassLevelNotFoundError
from app.features.subjects.exceptions import SubjectNotFoundError
from app.features.areas.exceptions import AreaNotFoundError
from app.features.areas.repository import AreaRepository
from app.db.unit_of_work import UnitOfWork
from app.features.users.model import User, UserRole
from app.features.class_levels.repository import ClassLevelRepository
from app.features.client_posts.model import ClientPost
from app.features.client_posts.repository import ClientPostRepository
from app.features.client_posts.schemas import ClientPostCreate, ClientPostUpdate
from app.features.client_profiles.model import ClientProfile
from app.features.client_profiles.repository import ClientProfileRepository
from app.features.subjects.model import Subject
from app.features.subjects.repository import SubjectRepository


class ClientPostService:
    def __init__(
        self,
        client_post_repository: ClientPostRepository,
        client_profile_repository: ClientProfileRepository,
        class_level_repository: ClassLevelRepository,
        subject_repository: SubjectRepository,
        area_repository: AreaRepository,
        uow: UnitOfWork,
    ):
        self.client_post_repository = client_post_repository
        self.client_profile_repository = client_profile_repository
        self.class_level_repository = class_level_repository
        self.subject_repository = subject_repository
        self.area_repository = area_repository
        self.uow = uow

    def create(self, user_id: int, data: ClientPostCreate) -> ClientPost:
        client_profile = self._get_client_profile_of_user(user_id)
        self._ensure_class_level_exists(data.class_level_id)
        self._ensure_area_exists(data.area_id)
        subjects = self._get_subjects(data.subject_ids)

        post = ClientPost(
            client_id=client_profile.id,
            subjects=subjects,
            **data.model_dump(exclude={"subject_ids"}),
        )

        with self.uow:
            post = self.client_post_repository.create(post)
        return post

    def get_post_for_viewer(self, post_id: int, viewer: User) -> ClientPost:
        post = self.get_post(post_id)
        self._ensure_can_view(viewer, post.client.user_id)
        return post

    def get_post(self, post_id: int) -> ClientPost:
        post = self.client_post_repository.get_by_id(post_id)
        if post is None:
            raise PostNotFoundError()
        return post

    def get_client_posts(self, user_id: int, viewer: User) -> list[ClientPost]:
        self._ensure_can_view(viewer, user_id)
        client_profile = self.client_profile_repository.get_by_user_id(user_id)
        if client_profile is None:
            raise ProfileNotFoundError("Client profile not found")
        return self.client_post_repository.get_by_client_id(client_profile.id)

    def get_my_posts(self, user_id: int) -> list[ClientPost]:
        client_profile = self._get_client_profile_of_user(user_id)
        return self.client_post_repository.get_by_client_id(client_profile.id)

    def update_post(
        self,
        user_id: int,
        post_id: int,
        data: ClientPostUpdate,
    ) -> ClientPost:
        post = self._get_own_post(user_id, post_id)
        values = data.model_dump(exclude_unset=True)

        if "area_id" in values:
            self._ensure_area_exists(values["area_id"])

        if "class_level_id" in values:
            self._ensure_class_level_exists(values["class_level_id"])

        if "subject_ids" in values:
            values["subjects"] = self._get_subjects(values.pop("subject_ids"))

        self._ensure_budget_range_is_valid(
            values.get("budget_min", post.budget_min),
            values.get("budget_max", post.budget_max),
        )

        with self.uow:
            post = self.client_post_repository.update(post, values)
        return post

    def delete_post(self, user_id: int, post_id: int) -> None:
        post = self._get_own_post(user_id, post_id)

        with self.uow:
            self.client_post_repository.delete(post)

    def _get_client_profile_of_user(self, user_id: int) -> ClientProfile:
        client_profile = self.client_profile_repository.get_by_user_id(user_id)
        if client_profile is None:
            raise ProfileNotFoundError("Client profile does not exist")
        return client_profile

    def _get_own_post(self, user_id: int, post_id: int) -> ClientPost:
        client_profile = self._get_client_profile_of_user(user_id)
        post = self.get_post(post_id)
        if post.client_id != client_profile.id:
            raise PostAccessDeniedError()
        return post

    def _ensure_class_level_exists(self, class_level_id: int) -> None:
        if self.class_level_repository.get_by_id(class_level_id) is None:
            raise ClassLevelNotFoundError()

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
    def _ensure_budget_range_is_valid(
        budget_min: Decimal | None,
        budget_max: Decimal | None,
    ) -> None:
        if budget_min is not None and budget_max is not None and budget_max < budget_min:
            raise ValidationException(
                details=[
                    {
                        "field": "budget_max",
                        "message": "must be greater than or equal to budget_min",
                    }
                ]
            )

    @staticmethod
    def _ensure_can_view(viewer: User, owner_user_id: int) -> None:
        if viewer.role == UserRole.CLIENT and viewer.id != owner_user_id:
            raise ViewAccessDeniedError("Clients can only view their own posts")

    def _ensure_area_exists(self, area_id: int) -> None:
        if self.area_repository.get_by_id(area_id) is None:
            raise AreaNotFoundError()
