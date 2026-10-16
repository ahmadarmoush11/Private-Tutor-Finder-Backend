from fastapi import APIRouter, status

from app.features.auth.dependencies import TutorUser
from app.features.tutor_requests.dependencies import TutorRequestServiceDep
from app.features.tutor_requests.schemas import TutorRequestCreate, TutorRequestResponse


router = APIRouter(prefix="/tutor-requests", tags=["Tutor Requests"])


@router.post(
    "",
    response_model=TutorRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_request(
    data: TutorRequestCreate,
    current_user: TutorUser,
    service: TutorRequestServiceDep,
):
    return service.create(current_user.id, data.client_post_id)


@router.get("", response_model=list[TutorRequestResponse])
def get_my_requests(
    current_user: TutorUser,
    service: TutorRequestServiceDep,
):
    return service.get_all_for_tutor(current_user.id)


@router.get("/{tutor_request_id}", response_model=TutorRequestResponse)
def get_request(
    tutor_request_id: int,
    current_user: TutorUser,
    service: TutorRequestServiceDep,
):
    return service.get_by_id_for_tutor(current_user.id, tutor_request_id)


@router.delete("/{tutor_request_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_request(
    tutor_request_id: int,
    current_user: TutorUser,
    service: TutorRequestServiceDep,
):
    service.delete_for_tutor(current_user.id, tutor_request_id)
