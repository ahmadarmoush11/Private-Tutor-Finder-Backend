from fastapi import APIRouter, status

from app.features.auth.dependencies import TutorUser
from app.features.applications.dependencies import ApplicationServiceDep
from app.features.applications.schemas import ApplicationCreate, ApplicationResponse


router = APIRouter(prefix="/applications", tags=["Applications"])


@router.post(
    "",
    response_model=ApplicationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_application(
    data: ApplicationCreate,
    current_user: TutorUser,
    service: ApplicationServiceDep,
):
    return service.create(current_user.id, data.client_post_id)


@router.get("", response_model=list[ApplicationResponse])
def get_my_applications(
    current_user: TutorUser,
    service: ApplicationServiceDep,
):
    return service.get_all_for_tutor(current_user.id)


@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(
    application_id: int,
    current_user: TutorUser,
    service: ApplicationServiceDep,
):
    return service.get_by_id_for_tutor(current_user.id, application_id)


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    application_id: int,
    current_user: TutorUser,
    service: ApplicationServiceDep,
):
    service.delete_for_tutor(current_user.id, application_id)
