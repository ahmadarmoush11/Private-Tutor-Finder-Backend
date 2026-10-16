from app.db.unit_of_work import UnitOfWork
from app.core.exceptions import (
    PostNotFoundError,
    RequestCannotBeDeletedError,
    RequestCannotBeUpdatedError,
    RequestNotFoundError,
)
from app.features.client_requests.exceptions import ClientRequestAlreadyExistsError
from app.features.client_requests.model import ClientRequest, RequestStatus
from app.features.tutor_posts.repository import TutorPostRepository
from app.features.client_requests.repository import ClientRequestRepository
from app.features.tutor_posts.service import TutorPostService
from app.features.client_profiles.service import ClientProfileService


class ClientRequestService:
    def __init__(
        self,
        client_request_repository: ClientRequestRepository,
        client_profile_service: ClientProfileService,
        tutor_post_repository: TutorPostRepository,
        tutor_post_service: TutorPostService,
        uow: UnitOfWork
            
    ):
        self.client_request_repository=client_request_repository
        self.client_profile_service=client_profile_service
        self.tutor_post_repository=tutor_post_repository
        self.tutor_post_service=tutor_post_service
        self.uow=uow
        


    def create(
        self,
        user_id: int,
        tutor_post_id: int,

    )->ClientRequest:

        self._check_post(tutor_post_id)
        client_profile=self.client_profile_service.get_by_user_id(user_id)
        self._check_existing_request_for_client(client_profile.id,tutor_post_id)

        client_request= ClientRequest(
            client_id=client_profile.id,
            tutor_post_id=tutor_post_id,
        )

        with self.uow:
            client_request=self.client_request_repository.create(client_request)

        return client_request

            

    def get_by_id_for_client(
        self,
        user_id: int,
        client_request_id: int,
    ) -> ClientRequest:
        client_request = self.client_request_repository.get_by_id_for_client(
            user_id,
            client_request_id,
        )
        if client_request is None:
            raise RequestNotFoundError()
        return client_request

    def get_by_id_for_tutor(
        self,
        user_id: int,
        client_request_id: int,
    ) -> ClientRequest:
        client_request = self.client_request_repository.get_by_id_for_tutor(
            user_id,
            client_request_id,
        )
        if client_request is None:
            raise RequestNotFoundError()
        return client_request

    

    def get_all_for_client(
        self,
        user_id: int,
    ) -> list[ClientRequest]:
        client_profile = self.client_profile_service.get_by_user_id(user_id)
        return self.client_request_repository.get_all_by_client_id(client_profile.id)

    def delete_for_client(
        self,
        user_id: int,
        client_request_id: int,
    ) -> None:
        client_request = self.get_by_id_for_client(user_id, client_request_id)

        if client_request.status in (RequestStatus.ACCEPTED, RequestStatus.CONFIRMED):
            raise RequestCannotBeDeletedError()

        with self.uow:
            self.client_request_repository.delete(client_request)


    def get_all_for_tutor(
        self,
        user_id: int,
    ) -> list[ClientRequest]:
        return self.client_request_repository.get_all_for_tutor(user_id)

    def accept_for_tutor(
        self,
        user_id: int,
        client_request_id: int,
    ) -> ClientRequest:
        return self._respond_for_tutor(user_id, client_request_id, RequestStatus.ACCEPTED)

    def reject_for_tutor(
        self,
        user_id: int,
        client_request_id: int,
    ) -> ClientRequest:
        return self._respond_for_tutor(user_id, client_request_id, RequestStatus.REJECTED)

    def _respond_for_tutor(
        self,
        user_id: int,
        client_request_id: int,
        new_status: RequestStatus,
    ) -> ClientRequest:
        client_request = self.get_by_id_for_tutor(user_id, client_request_id)

        if client_request.status != RequestStatus.PENDING:
            raise RequestCannotBeUpdatedError()

        with self.uow:
            client_request = self.client_request_repository.update_status(
                client_request,
                new_status,
            )
        return client_request

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

        existing_request=self.client_request_repository.get_existing(client_profile_id,tutor_post_id)

        if existing_request is not None:
            raise ClientRequestAlreadyExistsError()
