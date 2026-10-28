from typing import Annotated

from fastapi import APIRouter, Query

from app.features.auth.dependencies import AdminUser
from app.features.degree_verifications.dependencies import DegreeVerificationServiceDep
from app.features.degree_verifications.schemas import (
    DegreeVerificationAdminResponse,
    DegreeVerificationReview,
)
from app.shared.enums import VerificationStatus


router = APIRouter(
    prefix="/admin/degree-verifications",
    tags=["Degree Verification (Admin)"],
)


@router.get("", response_model=list[DegreeVerificationAdminResponse])
def get_degree_verifications(
    current_user: AdminUser,
    service: DegreeVerificationServiceDep,
    verification_status: Annotated[VerificationStatus | None, Query(alias="status")] = None,
    tutor_user_id: int | None = None,
):
    return service.get_all_for_admin(tutor_user_id, verification_status)


@router.get("/{degree_verification_id}", response_model=DegreeVerificationAdminResponse)
def get_degree_verification(
    degree_verification_id: int,
    current_user: AdminUser,
    service: DegreeVerificationServiceDep,
):
    return service.get_by_id_for_admin(degree_verification_id)


@router.post(
    "/{degree_verification_id}/review",
    response_model=DegreeVerificationAdminResponse,
)
def review_degree_verification(
    degree_verification_id: int,
    data: DegreeVerificationReview,
    current_user: AdminUser,
    service: DegreeVerificationServiceDep,
):
    return service.verify_degree(current_user.id, degree_verification_id, data)
