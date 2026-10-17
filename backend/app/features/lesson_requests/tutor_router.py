from fastapi import APIRouter

from app.features.auth.dependencies import TutorUser
from app.features.lesson_requests.dependencies import LessonRequestServiceDep
from app.features.lesson_requests.schemas import LessonRequestResponse


router = APIRouter(prefix="/tutors/me/lesson-requests", tags=["Lesson Requests (Tutor Inbox)"])


@router.get("", response_model=list[LessonRequestResponse])
def get_received_lesson_requests(
    current_user: TutorUser,
    service: LessonRequestServiceDep,
):
    return service.get_all_for_tutor(current_user.id)


@router.get("/{lesson_request_id}", response_model=LessonRequestResponse)
def get_received_lesson_request(
    lesson_request_id: int,
    current_user: TutorUser,
    service: LessonRequestServiceDep,
):
    return service.get_by_id_for_tutor(current_user.id, lesson_request_id)


@router.post("/{lesson_request_id}/accept", response_model=LessonRequestResponse)
def accept_lesson_request(
    lesson_request_id: int,
    current_user: TutorUser,
    service: LessonRequestServiceDep,
):
    return service.accept_for_tutor(current_user.id, lesson_request_id)


@router.post("/{lesson_request_id}/reject", response_model=LessonRequestResponse)
def reject_lesson_request(
    lesson_request_id: int,
    current_user: TutorUser,
    service: LessonRequestServiceDep,
):
    return service.reject_for_tutor(current_user.id, lesson_request_id)
