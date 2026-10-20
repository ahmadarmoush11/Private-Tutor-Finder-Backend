from fastapi import APIRouter

from app.features.auth.dependencies import ClientOrAdminUser, TutorUser
from app.features.tutor_reviews.dependencies import TutorReviewServiceDep
from app.features.tutor_reviews.schemas import TutorReviewResponse


router = APIRouter(prefix="/tutors", tags=["Tutor Reviews"])


@router.get("/me/reviews", response_model=list[TutorReviewResponse])
def get_my_received_reviews(
    current_user: TutorUser,
    service: TutorReviewServiceDep,
):
    return service.get_reviews_of_tutor(current_user.id)


@router.get("/{user_id}/reviews", response_model=list[TutorReviewResponse])
def get_tutor_reviews(
    user_id: int,
    current_user: ClientOrAdminUser,
    service: TutorReviewServiceDep,
):
    return service.get_reviews_of_tutor(user_id)
