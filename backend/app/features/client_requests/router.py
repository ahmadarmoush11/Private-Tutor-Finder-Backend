from fastapi import APIRouter, status

from app.features.auth.dependencies import ClientUser
from app.features.client_requests.dependencies import ClientRequestServiceDep
from app.features.client_requests.schemas import (
    ClientRequestCreate,
    ClientRequestResponse,
)


router = APIRouter(prefix="/client-requests", tags=["Clients Requests"])


@router.post(
    "",
    response_model=ClientRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_request(
    data: ClientRequestCreate,
    current_user: ClientUser,
    service: ClientRequestServiceDep,
):
    return service.create(current_user.id, data.tutor_post_id)


@router.get("", response_model=list[ClientRequestResponse])
def get_my_requests(
    current_user: ClientUser,
    service: ClientRequestServiceDep,
):
    return service.get_all_for_client(current_user.id)


@router.get("/{client_request_id}", response_model=ClientRequestResponse)
def get_request(
    client_request_id: int,
    current_user: ClientUser,
    service: ClientRequestServiceDep,
):
    return service.get_by_id_for_client(current_user.id, client_request_id)


@router.delete("/{client_request_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_request(
    client_request_id: int,
    current_user: ClientUser,
    service: ClientRequestServiceDep,
):
    service.delete_for_client(current_user.id, client_request_id)
