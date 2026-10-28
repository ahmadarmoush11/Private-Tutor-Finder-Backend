from datetime import datetime, timezone

from app.features.degree_verifications.model import DegreeVerification, DegreePhoto, NationalIdPhoto
from app.features.degree_verifications.schemas import (
    DegreeVerificationRequestCreate,
    DegreeVerificationReview,
)
from app.core.exceptions import ProfileNotFoundError
from app.features.degree_verifications.repository import DegreeVerificationRepository
from app.features.degree_verifications.exceptions import (
    DegreeVerificationRequestNotFound,
    DegreeVerificationResponseError,
    DegreeVerificationIsCancelledError,
    DegreeVerificationIsNotPendingError,
)
from app.features.tutor_profiles.model import TutorProfile
from app.db.unit_of_work import UnitOfWork
from app.shared.enums import VerificationStatus
from app.features.tutor_profiles.repository import TutorProfileRepository


class DegreeVerificationService:
    def __init__(
        self,
        degree_verification_repository: DegreeVerificationRepository,
        tutor_profile_repository: TutorProfileRepository,
        uow: UnitOfWork,
    ):
        self.degree_verification_repository=degree_verification_repository
        self.tutor_profile_repository= tutor_profile_repository
        self.uow=uow

    def create(
        self,
        user_id: int,
        degree_verification_request: DegreeVerificationRequestCreate
    )->DegreeVerification:

        tutor_profile=self._get_tutor_profile(user_id)

        degree_verification= DegreeVerification(
            tutor_profile_id= tutor_profile.id,
            degree= degree_verification_request.degree,
            degree_photos=[
                DegreePhoto(photo_path=photo.photo_path)
                for photo in degree_verification_request.degree_photos
            ],
            national_id_photos=[
                NationalIdPhoto(photo_path=photo.photo_path)
                for photo in degree_verification_request.national_id_photos
            ],
        )

        with self.uow:
            degree_verification=self.degree_verification_repository.create(degree_verification)

        return self.get_by_id_for_tutor(user_id, degree_verification.id)

    def verify_degree(
        self,
        admin_user_id: int,
        degree_verification_id: int,
        degree_verification_response: DegreeVerificationReview,
    )->DegreeVerification:

        degree_verification= self.get_by_id_for_admin(degree_verification_id)

        if degree_verification.status != VerificationStatus.PENDING:
            raise DegreeVerificationIsNotPendingError

        if degree_verification_response.status not in (
            VerificationStatus.VERIFIED,
            VerificationStatus.REJECTED,
        ):
            raise DegreeVerificationResponseError

        degree_verification.status = degree_verification_response.status
        degree_verification.reviewed_by_id = admin_user_id
        degree_verification.reviewed_at = datetime.now(timezone.utc)

        with self.uow:
            self.degree_verification_repository.verify(degree_verification)

        return self.get_by_id_for_admin(degree_verification_id)

    def cancel(
        self,
        user_id: int,
        degree_verification_id: int,
    )-> DegreeVerification:

        tutor_profile= self._get_tutor_profile(user_id)

        degree_verification= self.degree_verification_repository.get_by_id_for_tutor(tutor_profile.id, degree_verification_id)

        if degree_verification is None:
            raise DegreeVerificationRequestNotFound

        if degree_verification.status != VerificationStatus.PENDING:
            raise DegreeVerificationIsNotPendingError

        degree_verification.status= VerificationStatus.CANCELLED

        with self.uow:
            degree_verification= self.degree_verification_repository.update(degree_verification)

        return degree_verification


    def get_by_id_for_tutor(
        self,
        user_id: int,
        degree_verification_id: int,
    )->DegreeVerification:

        tutor_profile=self._get_tutor_profile(user_id)
        degree_verification= self.degree_verification_repository.get_by_id_for_tutor(tutor_profile.id, degree_verification_id)

        if degree_verification is None:
            raise DegreeVerificationRequestNotFound

        return degree_verification


    def get_by_id_for_admin(
        self,
        degree_verification_id: int,
    )->DegreeVerification:
        degree_verification= self.degree_verification_repository.get_by_id_for_admin(degree_verification_id)

        if degree_verification is None:
            raise DegreeVerificationRequestNotFound

        return degree_verification

    def get_all_for_admin(
        self,
        user_id: int | None,
        status: VerificationStatus | None
    )->list[DegreeVerification]:

        if status== VerificationStatus.CANCELLED:
            raise DegreeVerificationIsCancelledError

        tutor_profile_id = None

        if user_id is not None:
            tutor_profile_id = self._get_tutor_profile(user_id).id

        degree_verification_list= self.degree_verification_repository.get_all_for_admin(status, tutor_profile_id)

        if degree_verification_list is None:
            return []

        return degree_verification_list
    
        

    def get_all_for_tutor(
        self,
        user_id: int,
        status: VerificationStatus | None,
    )->list[DegreeVerification]:

        tutor_profile=self._get_tutor_profile(user_id)

        return self.degree_verification_repository.get_all_for_tutor(tutor_profile.id,status)
    

    def _get_tutor_profile(
        self,
        user_id: int,
    )->TutorProfile | None:

        tutor_profile= self.tutor_profile_repository.get_by_user_id(user_id)

        if tutor_profile is None:
            raise ProfileNotFoundError

        return tutor_profile


        

        

