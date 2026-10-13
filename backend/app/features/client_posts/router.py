from fastapi import APIRouter, status

from app.features.auth.dependencies import ClientUser, CurrentUser
from app.features.client_posts.dependencies import ClientPostServiceDep
from app.features.client_posts.schemas import (
    ClientPostCreate,
    ClientPostResponse,
    ClientPostUpdate,
)


router = APIRouter(prefix="/clients", tags=["Clients Posts"])


@router.post(
    "/posts",
    response_model=ClientPostResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_post(
    data: ClientPostCreate,
    current_user: ClientUser,
    service: ClientPostServiceDep,
):
    return service.create(current_user.id, data)


@router.get("/me/posts", response_model=list[ClientPostResponse])
def get_my_posts(
    current_user: ClientUser,
    service: ClientPostServiceDep,
):
    return service.get_my_posts(current_user.id)


@router.get(
    "/posts/{post_id}",
    response_model=ClientPostResponse,
)
def get_post(
    post_id: int,
    current_user: CurrentUser,
    service: ClientPostServiceDep,
):
    return service.get_post_for_viewer(post_id, current_user)


@router.get(
    "/{user_id}/posts",
    response_model=list[ClientPostResponse],
)
def get_client_posts(
    user_id: int,
    current_user: CurrentUser,
    service: ClientPostServiceDep,
):
    return service.get_client_posts(user_id, current_user)


@router.patch("/posts/{post_id}", response_model=ClientPostResponse)
def update_post(
    post_id: int,
    data: ClientPostUpdate,
    current_user: ClientUser,
    service: ClientPostServiceDep,
):
    return service.update_post(current_user.id, post_id, data)


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    current_user: ClientUser,
    service: ClientPostServiceDep,
):
    service.delete_post(current_user.id, post_id)
