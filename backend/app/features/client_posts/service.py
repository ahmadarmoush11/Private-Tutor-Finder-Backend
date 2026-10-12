from app.core.exceptions import (
    ClassLevelNotFoundError,
    PostAccessDeniedError,
    PostNotFoundError,
    ProfileNotFoundError,
)
from app.db.unit_of_work import UnitOfWork
from app.features.class_levels.repository import ClassLevelRepository
from app.features.client_posts.model import ClientPost
from app.features.client_posts.repository import ClientPostRepository
from app.features.client_posts.schemas import ClientPostCreate, ClientPostUpdate
from app.features.client_profiles.model import ClientProfile
from app.features.client_profiles.repository import ClientProfileRepository


class ClientPostService:
    def __init__(
        self,
        client_post_repository: ClientPostRepository,
        client_profile_repository: ClientProfileRepository,
        class_level_repository: ClassLevelRepository,
        uow: UnitOfWork,
    ):
        self.client_post_repository = client_post_repository
        self.client_profile_repository = client_profile_repository
        self.class_level_repository = class_level_repository
        self.uow = uow

    def create(self, user_id: int, data: ClientPostCreate) -> ClientPost:
        client_profile = self._get_client_profile_of_user(user_id)
        self._ensure_class_level_exists(data.class_level_id)

        post = ClientPost(client_id=client_profile.id, **data.model_dump())

        with self.uow:
            post = self.client_post_repository.create(post)
        return post

    def get_post(self, post_id: int) -> ClientPost:
        post = self.client_post_repository.get_by_id(post_id)
        if post is None:
            raise PostNotFoundError()
        return post

    def get_client_posts(self, client_id: int) -> list[ClientPost]:
        if self.client_profile_repository.get_client_profile(client_id) is None:
            raise ProfileNotFoundError("Client profile not found")
        return self.client_post_repository.get_by_client_id(client_id)

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

        if "class_level_id" in values:
            self._ensure_class_level_exists(values["class_level_id"])

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
