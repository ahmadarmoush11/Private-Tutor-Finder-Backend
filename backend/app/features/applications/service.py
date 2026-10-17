from app.core.exceptions import (
    PostNotFoundError,
    ProfileNotFoundError,
    RequestCannotBeDeletedError,
    RequestCannotBeUpdatedError,
    RequestNotFoundError,
)
from app.features.applications.exceptions import ApplicationAlreadyExistsError
from app.db.unit_of_work import UnitOfWork
from app.features.client_posts.repository import ClientPostRepository
from app.features.tutor_profiles.model import TutorProfile
from app.features.tutor_profiles.repository import TutorProfileRepository
from app.features.applications.model import Application
from app.features.applications.repository import ApplicationRepository
from app.shared.enums import RequestStatus


class ApplicationService:
    def __init__(
        self,
        application_repository: ApplicationRepository,
        tutor_profile_repository: TutorProfileRepository,
        client_post_repository: ClientPostRepository,
        uow: UnitOfWork,
    ):
        self.application_repository = application_repository
        self.tutor_profile_repository = tutor_profile_repository
        self.client_post_repository = client_post_repository
        self.uow = uow

    def create(self, user_id: int, client_post_id: int) -> Application:
        tutor_profile = self._get_tutor_profile_of_user(user_id)

        if self.client_post_repository.get_by_id(client_post_id) is None:
            raise PostNotFoundError()

        if self.application_repository.get_existing(tutor_profile.id, client_post_id):
            raise ApplicationAlreadyExistsError()

        application = Application(
            tutor_id=tutor_profile.id,
            client_post_id=client_post_id,
        )

        with self.uow:
            application = self.application_repository.create(application)
        return application

    def get_by_id_for_tutor(self, user_id: int, application_id: int) -> Application:
        application = self.application_repository.get_by_id_for_tutor(
            user_id,
            application_id,
        )
        if application is None:
            raise RequestNotFoundError()
        return application

    def get_all_for_tutor(self, user_id: int) -> list[Application]:
        tutor_profile = self._get_tutor_profile_of_user(user_id)
        return self.application_repository.get_all_for_tutor(tutor_profile.id)

    def delete_for_tutor(self, user_id: int, application_id: int) -> None:
        application = self.get_by_id_for_tutor(user_id, application_id)

        if application.status in (RequestStatus.ACCEPTED, RequestStatus.CONFIRMED):
            raise RequestCannotBeDeletedError()

        with self.uow:
            self.application_repository.delete(application)

    def get_by_id_for_client(self, user_id: int, application_id: int) -> Application:
        application = self.application_repository.get_by_id_for_client(
            user_id,
            application_id,
        )
        if application is None:
            raise RequestNotFoundError()
        return application

    def get_all_for_client(self, user_id: int) -> list[Application]:
        return self.application_repository.get_all_for_client(user_id)

    def accept_for_client(self, user_id: int, application_id: int) -> Application:
        return self._respond_for_client(user_id, application_id, RequestStatus.ACCEPTED)

    def reject_for_client(self, user_id: int, application_id: int) -> Application:
        return self._respond_for_client(user_id, application_id, RequestStatus.REJECTED)

    def _respond_for_client(
        self,
        user_id: int,
        application_id: int,
        new_status: RequestStatus,
    ) -> Application:
        application = self.get_by_id_for_client(user_id, application_id)

        if application.status != RequestStatus.PENDING:
            raise RequestCannotBeUpdatedError()

        with self.uow:
            application = self.application_repository.update_status(
                application,
                new_status,
            )
        return application

    def _get_tutor_profile_of_user(self, user_id: int) -> TutorProfile:
        tutor_profile = self.tutor_profile_repository.get_by_user_id(user_id)
        if tutor_profile is None:
            raise ProfileNotFoundError("Tutor profile not found")
        return tutor_profile
