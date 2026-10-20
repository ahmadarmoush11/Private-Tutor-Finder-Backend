from fastapi import APIRouter, status

from app.features.auth.dependencies import ClientUser
from app.features.tutor_reviews.dependencies import TutorReviewServiceDep
from app.features.tutor_reviews.schemas import (
    TutorReviewCreate,
    TutorReviewResponse,
    TutorReviewUpdate,
)


router = APIRouter(prefix="/tutor-reviews", tags=["Tutor Reviews"])


@router.post(
    "",
    response_model=TutorReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_review(
    data: TutorReviewCreate,
    current_user: ClientUser,
    service: TutorReviewServiceDep,
):
    return service.create(current_user.id, data)


@router.patch("/{tutor_review_id}", response_model=TutorReviewResponse)
def update_review(
    tutor_review_id: int,
    data: TutorReviewUpdate,
    current_user: ClientUser,
    service: TutorReviewServiceDep,
):
    return service.update(current_user.id, tutor_review_id, data)


@router.delete("/{tutor_review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    tutor_review_id: int,
    current_user: ClientUser,
    service: TutorReviewServiceDep,
):
    service.delete(current_user.id, tutor_review_id)
