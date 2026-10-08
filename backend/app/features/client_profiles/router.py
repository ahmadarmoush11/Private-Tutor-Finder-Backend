from fastapi import APIRouter, Depends, status

from app.features.auth.dependencies import ClientUser, require_admin
from app.features.client_profiles.dependencies import ClientProfileServiceDep
from app.features.client_profiles.schemas import (
    ClientProfileCreate,
    ClientProfileOut,
    ClientProfileUpdate,
)


router = APIRouter(prefix="/clients", tags=["clients"])


@router.post(
    "/me/profile",
    response_model=ClientProfileOut,
    status_code=status.HTTP_201_CREATED,
)
def create_my_profile(
    data: ClientProfileCreate,
    current_user: ClientUser,
    service: ClientProfileServiceDep,
):
    return service.create(current_user, data)


@router.get("/me/profile", response_model=ClientProfileOut)
def get_my_profile(current_user: ClientUser, service: ClientProfileServiceDep):
    return service.get_by_user_id(current_user.id)


@router.patch("/me/profile", response_model=ClientProfileOut)
def update_my_profile(
    data: ClientProfileUpdate,
    current_user: ClientUser,
    service: ClientProfileServiceDep,
):
    return service.update(current_user, data)


@router.get(
    "/{user_id}/profile",
    response_model=ClientProfileOut,
    dependencies=[Depends(require_admin)],
)
def get_client_profile(user_id: int, service: ClientProfileServiceDep):
    return service.get_by_user_id(user_id)
