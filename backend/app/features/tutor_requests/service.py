from app.core.exceptions import (
    PostNotFoundError,
    ProfileNotFoundError,
    TutorRequestAlreadyExistsError,
    TutorRequestCannotBeDeletedError,
    TutorRequestCannotBeUpdatedError,
    TutorRequestNotFoundError,
)
from app.db.unit_of_work import UnitOfWork
from app.features.client_posts.repository import ClientPostRepository
from app.features.tutor_profiles.model import TutorProfile
from app.features.tutor_profiles.repository import TutorProfileRepository
from app.features.tutor_requests.model import TutorRequest
from app.features.tutor_requests.repository import TutorRequestRepository
from app.shared.enums import RequestStatus


class TutorRequestService:
    def __init__(
        self,
        tutor_request_repository: TutorRequestRepository,
        tutor_profile_repository: TutorProfileRepository,
        client_post_repository: ClientPostRepository,
        uow: UnitOfWork,
    ):
        self.tutor_request_repository = tutor_request_repository
        self.tutor_profile_repository = tutor_profile_repository
        self.client_post_repository = client_post_repository
        self.uow = uow

    def create(self, user_id: int, client_post_id: int) -> TutorRequest:
        tutor_profile = self._get_tutor_profile_of_user(user_id)

        if self.client_post_repository.get_by_id(client_post_id) is None:
            raise PostNotFoundError()

        if self.tutor_request_repository.get_existing(tutor_profile.id, client_post_id):
            raise TutorRequestAlreadyExistsError()

        tutor_request = TutorRequest(
            tutor_id=tutor_profile.id,
            client_post_id=client_post_id,
        )

        with self.uow:
            tutor_request = self.tutor_request_repository.create(tutor_request)
        return tutor_request

    def get_by_id_for_tutor(self, user_id: int, tutor_request_id: int) -> TutorRequest:
        tutor_request = self.tutor_request_repository.get_by_id_for_tutor(
            user_id,
            tutor_request_id,
        )
        if tutor_request is None:
            raise TutorRequestNotFoundError()
        return tutor_request

    def get_all_for_tutor(self, user_id: int) -> list[TutorRequest]:
        tutor_profile = self._get_tutor_profile_of_user(user_id)
        return self.tutor_request_repository.get_all_for_tutor(tutor_profile.id)

    def delete_for_tutor(self, user_id: int, tutor_request_id: int) -> None:
        tutor_request = self.get_by_id_for_tutor(user_id, tutor_request_id)

        if tutor_request.status in (RequestStatus.ACCEPTED, RequestStatus.CONFIRMED):
            raise TutorRequestCannotBeDeletedError()

        with self.uow:
            self.tutor_request_repository.delete(tutor_request)

    def get_by_id_for_client(self, user_id: int, tutor_request_id: int) -> TutorRequest:
        tutor_request = self.tutor_request_repository.get_by_id_for_client(
            user_id,
            tutor_request_id,
        )
        if tutor_request is None:
            raise TutorRequestNotFoundError()
        return tutor_request

    def get_all_for_client(self, user_id: int) -> list[TutorRequest]:
        return self.tutor_request_repository.get_all_for_client(user_id)

    def accept_for_client(self, user_id: int, tutor_request_id: int) -> TutorRequest:
        return self._respond_for_client(user_id, tutor_request_id, RequestStatus.ACCEPTED)

    def reject_for_client(self, user_id: int, tutor_request_id: int) -> TutorRequest:
        return self._respond_for_client(user_id, tutor_request_id, RequestStatus.REJECTED)

    def _respond_for_client(
        self,
        user_id: int,
        tutor_request_id: int,
        new_status: RequestStatus,
    ) -> TutorRequest:
        tutor_request = self.get_by_id_for_client(user_id, tutor_request_id)

        if tutor_request.status != RequestStatus.PENDING:
            raise TutorRequestCannotBeUpdatedError()

        with self.uow:
            tutor_request = self.tutor_request_repository.update_status(
                tutor_request,
                new_status,
            )
        return tutor_request

    def _get_tutor_profile_of_user(self, user_id: int) -> TutorProfile:
        tutor_profile = self.tutor_profile_repository.get_by_user_id(user_id)
        if tutor_profile is None:
            raise ProfileNotFoundError("Tutor profile not found")
        return tutor_profile
