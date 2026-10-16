from fastapi import APIRouter

from app.features.auth.dependencies import ClientUser
from app.features.tutor_requests.dependencies import TutorRequestServiceDep
from app.features.tutor_requests.schemas import TutorRequestResponse


router = APIRouter(prefix="/clients/me/requests", tags=["Tutor Requests (Client Inbox)"])


@router.get("", response_model=list[TutorRequestResponse])
def get_received_requests(
    current_user: ClientUser,
    service: TutorRequestServiceDep,
):
    return service.get_all_for_client(current_user.id)


@router.get("/{tutor_request_id}", response_model=TutorRequestResponse)
def get_received_request(
    tutor_request_id: int,
    current_user: ClientUser,
    service: TutorRequestServiceDep,
):
    return service.get_by_id_for_client(current_user.id, tutor_request_id)


@router.post("/{tutor_request_id}/accept", response_model=TutorRequestResponse)
def accept_request(
    tutor_request_id: int,
    current_user: ClientUser,
    service: TutorRequestServiceDep,
):
    return service.accept_for_client(current_user.id, tutor_request_id)


@router.post("/{tutor_request_id}/reject", response_model=TutorRequestResponse)
def reject_request(
    tutor_request_id: int,
    current_user: ClientUser,
    service: TutorRequestServiceDep,
):
    return service.reject_for_client(current_user.id, tutor_request_id)
