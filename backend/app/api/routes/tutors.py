from fastapi import APIRouter, Depends, status

from app.api.deps import get_current_user, get_tutor_profile_service, require_tutor
from app.models.user import User
from app.schemas.tutor_profile import (
    TutorProfileCreate,
    TutorProfileOut,
    TutorProfileUpdate,
)
from app.services.tutor_profile_service import TutorProfileService


router = APIRouter(prefix="/tutors", tags=["tutors"])


@router.post(
    "/me/profile",
    response_model=TutorProfileOut,
    status_code=status.HTTP_201_CREATED,
)
def create_my_profile(
    data: TutorProfileCreate,
    current_user: User = Depends(require_tutor),
    service: TutorProfileService = Depends(get_tutor_profile_service),
):
    return service.create(current_user, data)


@router.get("/me/profile", response_model=TutorProfileOut)
def get_my_profile(
    current_user: User = Depends(require_tutor),
    service: TutorProfileService = Depends(get_tutor_profile_service),
):
    return service.get_by_user_id(current_user.id)


@router.patch("/me/profile", response_model=TutorProfileOut)
def update_my_profile(
    data: TutorProfileUpdate,
    current_user: User = Depends(require_tutor),
    service: TutorProfileService = Depends(get_tutor_profile_service),
):
    return service.update(current_user, data)


@router.get(
    "/{user_id}/profile",
    response_model=TutorProfileOut,
    dependencies=[Depends(get_current_user)],
)
def get_tutor_profile(
    user_id: int,
    service: TutorProfileService = Depends(get_tutor_profile_service),
):
    return service.get_by_user_id(user_id)
