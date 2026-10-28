from typing import Annotated

from fastapi import APIRouter, Query, status

from app.features.auth.dependencies import TutorUser
from app.features.degree_verifications.dependencies import DegreeVerificationServiceDep
from app.features.degree_verifications.schemas import (
    DegreeVerificationRequestCreate,
    DegreeVerificationResponse,
)
from app.shared.enums import VerificationStatus


router = APIRouter(prefix="/tutors/me/degree-verifications", tags=["Degree Verification"])


@router.post(
    "",
    response_model=DegreeVerificationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_degree_verification(
    data: DegreeVerificationRequestCreate,
    current_user: TutorUser,
    service: DegreeVerificationServiceDep,
):
    return service.create(current_user.id, data)


@router.get("", response_model=list[DegreeVerificationResponse])
def get_my_degree_verifications(
    current_user: TutorUser,
    service: DegreeVerificationServiceDep,
    verification_status: Annotated[VerificationStatus | None, Query(alias="status")] = None,
):
    return service.get_all_for_tutor(current_user.id, verification_status)


@router.get("/{degree_verification_id}", response_model=DegreeVerificationResponse)
def get_my_degree_verification(
    degree_verification_id: int,
    current_user: TutorUser,
    service: DegreeVerificationServiceDep,
):
    return service.get_by_id_for_tutor(current_user.id, degree_verification_id)


@router.post("/{degree_verification_id}/cancel", response_model=DegreeVerificationResponse)
def cancel_degree_verification(
    degree_verification_id: int,
    current_user: TutorUser,
    service: DegreeVerificationServiceDep,
):
    return service.cancel(current_user.id, degree_verification_id)
