from app.core.exceptions import (
    PostNotFoundError,
    ProfileNotFoundError,
    ViewAccessDeniedError,
)
from app.db.unit_of_work import UnitOfWork
from app.features.client_posts.model import ClientPost
from app.features.client_posts.repository import ClientPostRepository
from app.features.post_availabilities.exceptions import (
    AlreadyAvailableError,
    AvailabilityNotFoundError,
    PostNotActiveError,
)
from app.features.post_availabilities.model import PostAvailability
from app.features.post_availabilities.repository import PostAvailabilityRepository
from app.features.tutor_profiles.model import TutorProfile
from app.features.tutor_profiles.repository import TutorProfileRepository
from app.features.users.model import User, UserRole
from app.shared.enums import PostStatus


class PostAvailabilityService:
    def __init__(
        self,
        post_availability_repository: PostAvailabilityRepository,
        tutor_profile_repository: TutorProfileRepository,
        client_post_repository: ClientPostRepository,
        uow: UnitOfWork,
    ):
        self.post_availability_repository = post_availability_repository
        self.tutor_profile_repository = tutor_profile_repository
        self.client_post_repository = client_post_repository
        self.uow = uow

    def mark_available(self, user_id: int, post_id: int) -> PostAvailability:
        tutor_profile = self._get_tutor_profile_of_user(user_id)
        post = self._get_post(post_id)

        if post.status != PostStatus.ACTIVE:
            raise PostNotActiveError()
        if self.post_availability_repository.get(tutor_profile.id, post.id):
            raise AlreadyAvailableError()

        availability = PostAvailability(tutor_id=tutor_profile.id, client_post_id=post.id)
        with self.uow:
            self.post_availability_repository.create(availability)
        return self.post_availability_repository.get(tutor_profile.id, post.id)

    def withdraw(self, user_id: int, post_id: int) -> None:
        tutor_profile = self._get_tutor_profile_of_user(user_id)
        availability = self.post_availability_repository.get(tutor_profile.id, post_id)
        if availability is None:
            raise AvailabilityNotFoundError()

        with self.uow:
            self.post_availability_repository.delete(availability)

    def get_my_availabilities(self, user_id: int) -> list[PostAvailability]:
        tutor_profile = self._get_tutor_profile_of_user(user_id)
        return self.post_availability_repository.get_all_for_tutor(tutor_profile.id)

    def get_available_tutors(self, post_id: int, viewer: User) -> list[PostAvailability]:
        post = self._get_post(post_id)
        if viewer.role == UserRole.CLIENT and post.client.user_id != viewer.id:
            raise ViewAccessDeniedError("Clients can only view their own posts")
        return self.post_availability_repository.get_all_for_post(post.id)

    def _get_tutor_profile_of_user(self, user_id: int) -> TutorProfile:
        tutor_profile = self.tutor_profile_repository.get_by_user_id(user_id)
        if tutor_profile is None:
            raise ProfileNotFoundError("Tutor profile not found")
        return tutor_profile

    def _get_post(self, post_id: int) -> ClientPost:
        post = self.client_post_repository.get_by_id(post_id)
        if post is None:
            raise PostNotFoundError()
        return post
