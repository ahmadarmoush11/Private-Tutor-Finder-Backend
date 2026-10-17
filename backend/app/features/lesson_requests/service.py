from app.db.unit_of_work import UnitOfWork
from app.core.exceptions import (
    PostNotFoundError,
    RequestCannotBeDeletedError,
    RequestCannotBeUpdatedError,
    RequestNotFoundError,
)
from app.features.lesson_requests.exceptions import LessonRequestAlreadyExistsError
from app.features.lesson_requests.model import LessonRequest, RequestStatus
from app.features.tutor_posts.repository import TutorPostRepository
from app.features.lesson_requests.repository import LessonRequestRepository
from app.features.tutor_posts.service import TutorPostService
from app.features.client_profiles.service import ClientProfileService


class LessonRequestService:
    def __init__(
        self,
        lesson_request_repository: LessonRequestRepository,
        client_profile_service: ClientProfileService,
        tutor_post_repository: TutorPostRepository,
        tutor_post_service: TutorPostService,
        uow: UnitOfWork
            
    ):
        self.lesson_request_repository=lesson_request_repository
        self.client_profile_service=client_profile_service
        self.tutor_post_repository=tutor_post_repository
        self.tutor_post_service=tutor_post_service
        self.uow=uow
        


    def create(
        self,
        user_id: int,
        tutor_post_id: int,

    )->LessonRequest:

        self._check_post(tutor_post_id)
        client_profile=self.client_profile_service.get_by_user_id(user_id)
        self._check_existing_request_for_client(client_profile.id,tutor_post_id)

        lesson_request= LessonRequest(
            client_id=client_profile.id,
            tutor_post_id=tutor_post_id,
        )

        with self.uow:
            lesson_request=self.lesson_request_repository.create(lesson_request)

        return lesson_request

            

    def get_by_id_for_client(
        self,
        user_id: int,
        lesson_request_id: int,
    ) -> LessonRequest:
        lesson_request = self.lesson_request_repository.get_by_id_for_client(
            user_id,
            lesson_request_id,
        )
        if lesson_request is None:
            raise RequestNotFoundError()
        return lesson_request

    def get_by_id_for_tutor(
        self,
        user_id: int,
        lesson_request_id: int,
    ) -> LessonRequest:
        lesson_request = self.lesson_request_repository.get_by_id_for_tutor(
            user_id,
            lesson_request_id,
        )
        if lesson_request is None:
            raise RequestNotFoundError()
        return lesson_request

    

    def get_all_for_client(
        self,
        user_id: int,
    ) -> list[LessonRequest]:
        client_profile = self.client_profile_service.get_by_user_id(user_id)
        return self.lesson_request_repository.get_all_by_client_id(client_profile.id)

    def delete_for_client(
        self,
        user_id: int,
        lesson_request_id: int,
    ) -> None:
        lesson_request = self.get_by_id_for_client(user_id, lesson_request_id)

        if lesson_request.status in (RequestStatus.ACCEPTED, RequestStatus.CONFIRMED):
            raise RequestCannotBeDeletedError()

        with self.uow:
            self.lesson_request_repository.delete(lesson_request)


    def get_all_for_tutor(
        self,
        user_id: int,
    ) -> list[LessonRequest]:
        return self.lesson_request_repository.get_all_for_tutor(user_id)

    def accept_for_tutor(
        self,
        user_id: int,
        lesson_request_id: int,
    ) -> LessonRequest:
        return self._respond_for_tutor(user_id, lesson_request_id, RequestStatus.ACCEPTED)

    def reject_for_tutor(
        self,
        user_id: int,
        lesson_request_id: int,
    ) -> LessonRequest:
        return self._respond_for_tutor(user_id, lesson_request_id, RequestStatus.REJECTED)

    def _respond_for_tutor(
        self,
        user_id: int,
        lesson_request_id: int,
        new_status: RequestStatus,
    ) -> LessonRequest:
        lesson_request = self.get_by_id_for_tutor(user_id, lesson_request_id)

        if lesson_request.status != RequestStatus.PENDING:
            raise RequestCannotBeUpdatedError()

        with self.uow:
            lesson_request = self.lesson_request_repository.update_status(
                lesson_request,
                new_status,
            )
        return lesson_request

    def _check_post(
        self,
        tutor_post_id: int,
    )->None:
        tutor_post=self.tutor_post_repository.get_by_id(tutor_post_id)

        if tutor_post is None:
            raise PostNotFoundError()


    def _check_existing_request_for_client(
        self,
        client_profile_id: int,
        tutor_post_id: int,
    )->None:

        existing_request=self.lesson_request_repository.get_existing(client_profile_id,tutor_post_id)

        if existing_request is not None:
            raise LessonRequestAlreadyExistsError()
