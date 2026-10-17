from fastapi import APIRouter, status

from app.features.auth.dependencies import ClientUser
from app.features.lesson_requests.dependencies import LessonRequestServiceDep
from app.features.lesson_requests.schemas import (
    LessonRequestCreate,
    LessonRequestResponse,
)


router = APIRouter(prefix="/lesson-requests", tags=["Lesson Requests"])


@router.post(
    "",
    response_model=LessonRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_lesson_request(
    data: LessonRequestCreate,
    current_user: ClientUser,
    service: LessonRequestServiceDep,
):
    return service.create(current_user.id, data.tutor_post_id)


@router.get("", response_model=list[LessonRequestResponse])
def get_my_lesson_requests(
    current_user: ClientUser,
    service: LessonRequestServiceDep,
):
    return service.get_all_for_client(current_user.id)


@router.get("/{lesson_request_id}", response_model=LessonRequestResponse)
def get_lesson_request(
    lesson_request_id: int,
    current_user: ClientUser,
    service: LessonRequestServiceDep,
):
    return service.get_by_id_for_client(current_user.id, lesson_request_id)


@router.delete("/{lesson_request_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lesson_request(
    lesson_request_id: int,
    current_user: ClientUser,
    service: LessonRequestServiceDep,
):
    service.delete_for_client(current_user.id, lesson_request_id)
