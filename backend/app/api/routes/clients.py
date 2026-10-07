from fastapi import APIRouter, Depends, status

from app.api.deps import get_client_profile_service, require_admin, require_client
from app.models.user import User
from app.schemas.client_profile import (
    ClientProfileCreate,
    ClientProfileOut,
    ClientProfileUpdate,
)
from app.services.client_profile_service import ClientProfileService


router = APIRouter(prefix="/clients", tags=["clients"])


@router.post(
    "/me/profile",
    response_model=ClientProfileOut,
    status_code=status.HTTP_201_CREATED,
)
def create_my_profile(
    data: ClientProfileCreate,
    current_user: User = Depends(require_client),
    service: ClientProfileService = Depends(get_client_profile_service),
):
    return service.create(current_user, data)


@router.get("/me/profile", response_model=ClientProfileOut)
def get_my_profile(
    current_user: User = Depends(require_client),
    service: ClientProfileService = Depends(get_client_profile_service),
):
    return service.get_by_user_id(current_user.id)


@router.patch("/me/profile", response_model=ClientProfileOut)
def update_my_profile(
    data: ClientProfileUpdate,
    current_user: User = Depends(require_client),
    service: ClientProfileService = Depends(get_client_profile_service),
):
    return service.update(current_user, data)


@router.get(
    "/{user_id}/profile",
    response_model=ClientProfileOut,
    dependencies=[Depends(require_admin)],
)
def get_client_profile(
    user_id: int,
    service: ClientProfileService = Depends(get_client_profile_service),
):
    return service.get_by_user_id(user_id)
