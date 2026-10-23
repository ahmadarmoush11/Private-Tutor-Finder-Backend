from app.core.exceptions import (
    ProfileNotFoundError,
    RequestCannotBeDeletedError,
    RequestCannotBeUpdatedError,
    RequestNotFoundError,
)
from app.db.unit_of_work import UnitOfWork
from app.features.class_levels.exceptions import ClassLevelNotFoundError
from app.features.class_levels.repository import ClassLevelRepository
from app.features.client_profiles.service import ClientProfileService
from app.features.lesson_requests.exceptions import LessonRequestAlreadyExistsError
from app.features.lesson_requests.model import LessonRequest
from app.features.lesson_requests.repository import LessonRequestRepository
from app.features.lesson_requests.schemas import LessonRequestCreate
from app.features.subjects.exceptions import SubjectNotFoundError
from app.features.subjects.model import Subject
from app.features.subjects.repository import SubjectRepository
from app.features.tutor_profiles.model import TutorProfile
from app.features.tutor_profiles.repository import TutorProfileRepository
from app.shared.enums import RequestStatus
from app.features.notifications.service import NotificationService



class LessonRequestService:
    def __init__(
        self,
        lesson_request_repository: LessonRequestRepository,
        client_profile_service: ClientProfileService,
        tutor_profile_repository: TutorProfileRepository,
        subject_repository: SubjectRepository,
        class_level_repository: ClassLevelRepository,
        notification_service: NotificationService,
        uow: UnitOfWork,
    ):
        self.lesson_request_repository = lesson_request_repository
        self.client_profile_service = client_profile_service
        self.tutor_profile_repository = tutor_profile_repository
        self.subject_repository = subject_repository
        self.class_level_repository = class_level_repository
        self.notification_service=notification_service
        self.uow = uow

    def create(self, user_id: int, data: LessonRequestCreate) -> LessonRequest:
        client_profile = self.client_profile_service.get_by_user_id(user_id)
        tutor_profile = self._get_tutor_profile(data.tutor_user_id)
        subjects = self._get_subjects(data.subject_ids)
        self._ensure_class_level_exists(data.class_level_id)

        if self.lesson_request_repository.get_pending(client_profile.id, tutor_profile.id):
            raise LessonRequestAlreadyExistsError()

        lesson_request = LessonRequest(
            client_id=client_profile.id,
            tutor_id=tutor_profile.id,
            class_level_id=data.class_level_id,
            subjects=subjects,
            lesson_location=data.lesson_location,
            message=data.message,
        )


        with self.uow:
            lesson_request = self.lesson_request_repository.create(lesson_request)
            self.notification_service.create_for_lesson_request_received(lesson_request)
        return lesson_request

    def get_by_id_for_client(self, user_id: int, lesson_request_id: int) -> LessonRequest:
        lesson_request = self.lesson_request_repository.get_by_id_for_client(
            user_id,
            lesson_request_id,
        )
        if lesson_request is None:
            raise RequestNotFoundError()
        return lesson_request

    def get_by_id_for_tutor(self, user_id: int, lesson_request_id: int) -> LessonRequest:
        lesson_request = self.lesson_request_repository.get_by_id_for_tutor(
            user_id,
            lesson_request_id,
        )
        if lesson_request is None:
            raise RequestNotFoundError()
        return lesson_request

    def get_all_for_client(self, user_id: int) -> list[LessonRequest]:
        client_profile = self.client_profile_service.get_by_user_id(user_id)
        return self.lesson_request_repository.get_all_for_client(client_profile.id)

    def get_all_for_tutor(self, user_id: int) -> list[LessonRequest]:
        return self.lesson_request_repository.get_all_for_tutor(user_id)

    def delete_for_client(self, user_id: int, lesson_request_id: int) -> None:
        lesson_request = self.get_by_id_for_client(user_id, lesson_request_id)

        if lesson_request.status in (RequestStatus.ACCEPTED, RequestStatus.CONFIRMED):
            raise RequestCannotBeDeletedError()

        with self.uow:
            self.lesson_request_repository.delete(lesson_request)

    def accept_for_tutor(self, user_id: int, lesson_request_id: int) -> LessonRequest:
        return self._respond_for_tutor(user_id, lesson_request_id, RequestStatus.ACCEPTED)

    def reject_for_tutor(self, user_id: int, lesson_request_id: int) -> LessonRequest:
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

            if new_status==RequestStatus.ACCEPTED:
                self.notification_service.create_for_lesson_request_accepted(lesson_request)
            elif new_status==RequestStatus.REJECTED:
                self.notification_service.create_for_lesson_request_rejected(lesson_request)

        return lesson_request

    def _get_tutor_profile(self, tutor_user_id: int) -> TutorProfile:
        tutor_profile = self.tutor_profile_repository.get_by_user_id(tutor_user_id)
        if tutor_profile is None:
            raise ProfileNotFoundError("Tutor not found")
        return tutor_profile

    def _get_subjects(self, subject_ids: list[int]) -> list[Subject]:
        subjects = self.subject_repository.get_by_ids(subject_ids)
        found_ids = {subject.id for subject in subjects}
        missing_ids = [
            subject_id for subject_id in subject_ids if subject_id not in found_ids
        ]
        if missing_ids:
            raise SubjectNotFoundError(details={"missing_ids": missing_ids})
        return subjects

    def _ensure_class_level_exists(self, class_level_id: int) -> None:
        if self.class_level_repository.get_by_id(class_level_id) is None:
            raise ClassLevelNotFoundError()
