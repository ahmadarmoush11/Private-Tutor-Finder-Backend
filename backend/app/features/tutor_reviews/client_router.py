from fastapi import APIRouter

from app.features.auth.dependencies import ClientUser
from app.features.tutor_reviews.dependencies import TutorReviewServiceDep
from app.features.tutor_reviews.schemas import TutorReviewResponse


router = APIRouter(prefix="/clients/me/reviews", tags=["Tutor Reviews"])


@router.get("", response_model=list[TutorReviewResponse])
def get_my_reviews(
    current_user: ClientUser,
    service: TutorReviewServiceDep,
):
    return service.get_my_reviews(current_user.id)
