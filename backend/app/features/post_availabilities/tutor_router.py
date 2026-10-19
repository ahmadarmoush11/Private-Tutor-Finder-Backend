from fastapi import APIRouter

from app.features.auth.dependencies import TutorUser
from app.features.post_availabilities.dependencies import PostAvailabilityServiceDep
from app.features.post_availabilities.schemas import TutorAvailabilityResponse


router = APIRouter(prefix="/tutors/me/availabilities", tags=["Post Availability"])


@router.get("", response_model=list[TutorAvailabilityResponse])
def get_my_availabilities(
    current_user: TutorUser,
    service: PostAvailabilityServiceDep,
):
    return service.get_my_availabilities(current_user.id)
