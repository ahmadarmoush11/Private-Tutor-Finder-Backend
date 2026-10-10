from fastapi import APIRouter, Depends, status

from app.features.auth.dependencies import TutorUser, get_current_user
from app.features.tutor_posts.dependencies import TutorPostServiceDep
from app.features.tutor_posts.schemas import (
    TutorPostCreate,
    TutorPostResponse,
    TutorPostUpdate,
)


router = APIRouter(prefix="/tutors", tags=["Tutors Posts"])


@router.post(
    "/posts",
    response_model=TutorPostResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_post(
    data: TutorPostCreate,
    current_user: TutorUser,
    service: TutorPostServiceDep,
):
    return service.create(current_user.id, data)


@router.get("/me/posts", response_model=list[TutorPostResponse])
def get_my_posts(
    current_user: TutorUser,
    service: TutorPostServiceDep,
):
    return service.get_my_posts(current_user.id)


@router.get(
    "/posts/{post_id}",
    response_model=TutorPostResponse,
    dependencies=[Depends(get_current_user)],
)
def get_post(
    post_id: int,
    service: TutorPostServiceDep,
):
    return service.get_post(post_id)


@router.get(
    "/{tutor_id}/posts",
    response_model=list[TutorPostResponse],
    dependencies=[Depends(get_current_user)],
)
def get_tutor_posts(
    tutor_id: int,
    service: TutorPostServiceDep,
):
    return service.get_tutor_posts(tutor_id)


@router.patch("/posts/{post_id}", response_model=TutorPostResponse)
def update_post(
    post_id: int,
    data: TutorPostUpdate,
    current_user: TutorUser,
    service: TutorPostServiceDep,
):
    return service.update_post(current_user.id, post_id, data)


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    current_user: TutorUser,
    service: TutorPostServiceDep,
):
    service.delete_post(current_user.id, post_id)
