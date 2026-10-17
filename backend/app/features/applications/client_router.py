from fastapi import APIRouter

from app.features.auth.dependencies import ClientUser
from app.features.applications.dependencies import ApplicationServiceDep
from app.features.applications.schemas import ApplicationResponse


router = APIRouter(prefix="/clients/me/applications", tags=["Applications (Client Inbox)"])


@router.get("", response_model=list[ApplicationResponse])
def get_received_applications(
    current_user: ClientUser,
    service: ApplicationServiceDep,
):
    return service.get_all_for_client(current_user.id)


@router.get("/{application_id}", response_model=ApplicationResponse)
def get_received_application(
    application_id: int,
    current_user: ClientUser,
    service: ApplicationServiceDep,
):
    return service.get_by_id_for_client(current_user.id, application_id)


@router.post("/{application_id}/accept", response_model=ApplicationResponse)
def accept_application(
    application_id: int,
    current_user: ClientUser,
    service: ApplicationServiceDep,
):
    return service.accept_for_client(current_user.id, application_id)


@router.post("/{application_id}/reject", response_model=ApplicationResponse)
def reject_application(
    application_id: int,
    current_user: ClientUser,
    service: ApplicationServiceDep,
):
    return service.reject_for_client(current_user.id, application_id)
