from typing import Annotated

from fastapi import APIRouter, Query, status

from app.features.auth.dependencies import ClientOrAdminUser, TutorUser
from app.features.tutor_profiles.dependencies import TutorProfileServiceDep
from app.features.tutor_profiles.schemas import (
    TutorProfileCreate,
    TutorProfileDetailOut,
    TutorProfileOut,
    TutorProfileUpdate,
    TutorSearchParams,
)


router = APIRouter(prefix="/tutors", tags=["tutors"])


@router.get("", response_model=list[TutorProfileOut])
def search_tutors(
    params: Annotated[TutorSearchParams, Query()],
    current_user: ClientOrAdminUser,
    service: TutorProfileServiceDep,
):
    return service.search(params)


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


@router.get("/me/profile", response_model=TutorProfileDetailOut)
def get_my_profile(current_user: TutorUser, service: TutorProfileServiceDep):
    return service.get_profile_details(current_user.id)


@router.patch("/me/profile", response_model=TutorProfileOut)
def update_my_profile(
    data: TutorProfileUpdate,
    current_user: TutorUser,
    service: TutorProfileServiceDep,
):
    return service.update(current_user, data)


@router.get(
    "/{user_id}/profile",
    response_model=TutorProfileDetailOut,
)
def get_tutor_profile(
    user_id: int,
    current_user: ClientOrAdminUser,
    service: TutorProfileServiceDep,
):
    return service.get_profile_details(user_id)
