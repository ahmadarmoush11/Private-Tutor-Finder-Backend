from fastapi import APIRouter

from app.features.auth.dependencies import TutorUser
from app.features.client_requests.dependencies import ClientRequestServiceDep
from app.features.client_requests.schemas import ClientRequestResponse


router = APIRouter(prefix="/tutors/me/requests", tags=["Client Requests (Tutor Inbox)"])


@router.get("", response_model=list[ClientRequestResponse])
def get_received_requests(
    current_user: TutorUser,
    service: ClientRequestServiceDep,
):
    return service.get_all_for_tutor(current_user.id)


@router.get("/{client_request_id}", response_model=ClientRequestResponse)
def get_received_request(
    client_request_id: int,
    current_user: TutorUser,
    service: ClientRequestServiceDep,
):
    return service.get_by_id_for_tutor(current_user.id, client_request_id)


@router.post("/{client_request_id}/accept", response_model=ClientRequestResponse)
def accept_request(
    client_request_id: int,
    current_user: TutorUser,
    service: ClientRequestServiceDep,
):
    return service.accept_for_tutor(current_user.id, client_request_id)


@router.post("/{client_request_id}/reject", response_model=ClientRequestResponse)
def reject_request(
    client_request_id: int,
    current_user: TutorUser,
    service: ClientRequestServiceDep,
):
    return service.reject_for_tutor(current_user.id, client_request_id)
