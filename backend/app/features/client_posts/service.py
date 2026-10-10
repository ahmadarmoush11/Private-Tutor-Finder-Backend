from app.core.exceptions import(
    NotFoundException,
    BadRequestException,
    ConflictException,
    ProfileNotFoundError,
    PostNotFoundError,
    PostAccessDeniedError,
    ClassLevelNotFoundError,
)

from app.features.client_posts.repository import ClientPostRepository
from app.features.client_posts.schemas import(
    ClientPostCreate,
    ClientPostResponse,
    ClientPostUpdate,
)
from app.features.client_posts.model import ClientPost
from app.features.client_profiles.repository import ClientProfileRepository
from app.db.unit_of_work import UnitOfWork
from app.features.class_levels.repository import ClassLevelRepository


class ClientPostService:
    def __init__(
        self, 
        client_post_repository:ClientPostRepository,
        client_profile_repository: ClientProfileRepository,
        class_level_repository: ClassLevelRepository,
        uow: UnitOfWork,
    ):
        self.client_post_repository=client_post_repository
        self.client_profile_repository=client_profile_repository
        self.class_level_repository=class_level_repository
        self.uow=uow


    def create(
        self,
        user_id: int,
        post:ClientPostCreate,
    )->ClientPostCreate:
        client_profile=self.client_profile_repository.get_by_user_id(user_id)

        if client_profile is None:
            raise ProfileNotFoundError("Client profile does not exist")

        self._ensure_class_level_exists(post.class_level_id)

        new_post=ClientPost(
            client_id=client_profile.id,
            class_level_id=post.class_level_id,
            school_name=post.school_name if post.school_name else None,
            lesson_location=post.lesson_location,
            location=post.location if post.location else None,
            address_details=post.address_details,
            phone_number=post.phone_number,
            description=post.description,
        )

        with self.uow:
            new_post = self.client_post_repository.add_post(new_post)
        return new_post

    

    def get_post(
        self,
        post_id: int,
    )->ClientPostResponse:
        post=self.client_post_repository.get_post_by_id(post_id)

        if post is None:
            raise NotFoundException(
                message="POST_NOT_FOUND",
                details="This post does not exist"
            )

        return ClientPostResponse(
            post_id=post.id,
            client_id=post.client_id,
            class_level_id=post.class_level_id,
            school_name= post.school_name,
            lesson_location=post.lesson_location,
            status=post.status,
            location=post.location,
            address_details= post.address_details,
            phone_number= post.phone_number,
            description= post.description,

        )


    def get_client_posts(
        self,
        client_id: int,
    )->list[ClientPostResponse]:

        client=self.client_profile_repository.get_client_profile(client_id)

        if client is None:
            raise ProfileNotFoundError("Profile does not exist")

        posts=self.client_post_repository.get_client_posts(client_id)

        if posts is None:
            return []

        list_of_posts=[]
        for post in posts:
            current_post=ClientPostResponse(
            post_id=post.id,
            client_id=post.client_id,
            class_level_id=post.class_level_id,
            school_name= post.school_name,
            lesson_location=post.lesson_location,
            status=post.status,
            location=post.location,
            address_details= post.address_details,
            phone_number= post.phone_number,
            description= post.description,

            )
            list_of_posts.append(current_post)

        return list_of_posts


    def get_my_posts(
        self,
        user_id: int,
    ) -> list[ClientPostResponse]:
        client_profile = self.client_profile_repository.get_by_user_id(user_id)
        if client_profile is None:
            raise ProfileNotFoundError("Client profile does not exist")

        posts = self.client_post_repository.get_client_posts(client_profile.id)
        return [self._to_response(post) for post in posts]

    def update_post(
        self,
        user_id: int,
        post_id: int,
        data: ClientPostUpdate,
    ) -> ClientPostResponse:
        post = self._get_own_post(user_id, post_id)
        values = data.model_dump(exclude_unset=True)

        if "class_level_id" in values:
            self._ensure_class_level_exists(values["class_level_id"])

        with self.uow:
            post = self.client_post_repository.update(post, values)

        return self._to_response(post)

    def delete_post(
        self,
        user_id: int,
        post_id: int,
    ) -> None:
        post = self._get_own_post(user_id, post_id)

        with self.uow:
            self.client_post_repository.delete(post)

    def _get_own_post(
        self,
        user_id: int,
        post_id: int,
    ) -> ClientPost:
        client_profile = self.client_profile_repository.get_by_user_id(user_id)
        if client_profile is None:
            raise ProfileNotFoundError("Client profile does not exist")

        post = self.client_post_repository.get_post_by_id(post_id)
        if post is None:
            raise PostNotFoundError()

        if post.client_id != client_profile.id:
            raise PostAccessDeniedError()

        return post

    def _ensure_class_level_exists(
        self,
        class_level_id: int,
    ) -> None:
        if self.class_level_repository.get_by_id(class_level_id) is None:
            raise ClassLevelNotFoundError()

    @staticmethod
    def _to_response(post: ClientPost) -> ClientPostResponse:
        return ClientPostResponse(
            post_id=post.id,
            client_id=post.client_id,
            class_level_id=post.class_level_id,
            school_name=post.school_name,
            lesson_location=post.lesson_location,
            status=post.status,
            location=post.location,
            address_details=post.address_details,
            phone_number=post.phone_number,
            description=post.description,
        )
