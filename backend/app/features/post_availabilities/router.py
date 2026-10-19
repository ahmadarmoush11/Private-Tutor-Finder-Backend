from fastapi import APIRouter, status

from app.features.auth.dependencies import ClientOrAdminUser, TutorUser
from app.features.post_availabilities.dependencies import PostAvailabilityServiceDep
from app.features.post_availabilities.schemas import (
    AvailableTutorResponse,
    TutorAvailabilityResponse,
)


router = APIRouter(prefix="/clients/posts", tags=["Post Availability"])


@router.post(
    "/{post_id}/availability",
    response_model=TutorAvailabilityResponse,
    status_code=status.HTTP_201_CREATED,
)
def mark_available(
    post_id: int,
    current_user: TutorUser,
    service: PostAvailabilityServiceDep,
):
    return service.mark_available(current_user.id, post_id)


@router.delete("/{post_id}/availability", status_code=status.HTTP_204_NO_CONTENT)
def withdraw_availability(
    post_id: int,
    current_user: TutorUser,
    service: PostAvailabilityServiceDep,
):
    service.withdraw(current_user.id, post_id)


@router.get("/{post_id}/available-tutors", response_model=list[AvailableTutorResponse])
def get_available_tutors(
    post_id: int,
    current_user: ClientOrAdminUser,
    service: PostAvailabilityServiceDep,
):
    return service.get_available_tutors(post_id, current_user)
