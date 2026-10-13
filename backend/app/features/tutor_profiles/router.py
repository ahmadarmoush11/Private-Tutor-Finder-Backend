from fastapi import APIRouter, status

from app.features.auth.dependencies import CurrentUser, TutorUser
from app.features.tutor_profiles.dependencies import TutorProfileServiceDep
from app.features.tutor_profiles.schemas import (
    TutorProfileCreate,
    TutorProfileOut,
    TutorProfileUpdate,
)


router = APIRouter(prefix="/tutors", tags=["tutors"])


@router.post(
    "/me/profile",
    response_model=TutorProfileOut,
    status_code=status.HTTP_201_CREATED,
)
def create_my_profile(
    data: TutorProfileCreate,
    current_user: TutorUser,
    service: TutorProfileServiceDep,
):
    return service.create(current_user, data)


@router.get("/me/profile", response_model=TutorProfileOut)
def get_my_profile(current_user: TutorUser, service: TutorProfileServiceDep):
    return service.get_by_user_id(current_user.id)


@router.patch("/me/profile", response_model=TutorProfileOut)
def update_my_profile(
    data: TutorProfileUpdate,
    current_user: TutorUser,
    service: TutorProfileServiceDep,
):
    return service.update(current_user, data)


@router.get(
    "/{user_id}/profile",
    response_model=TutorProfileOut,
)
def get_tutor_profile(
    user_id: int,
    current_user: CurrentUser,
    service: TutorProfileServiceDep,
):
    return service.get_profile_for_viewer(user_id, current_user)
