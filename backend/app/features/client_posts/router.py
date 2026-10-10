from fastapi import APIRouter, status, Depends
from app.features.auth.dependencies import ClientUser, get_current_user
from app.features.client_posts.dependencies import ClientPostServiceDep
from app.features.client_posts.schemas import (
    ClientPostCreate,
    ClientPostResponse,
    ClientPostUpdate,
)



router = APIRouter(prefix="/clients", tags=["Clients Posts"])


@router.post(
    "/posts",
    status_code=status.HTTP_201_CREATED,
)
def create_post(
    data: ClientPostCreate,
    current_user: ClientUser,
    service: ClientPostServiceDep,
):
    return service.create(current_user.id, data)


@router.get(
    "/me/posts",
    response_model=list[ClientPostResponse],
)
def get_my_posts(
    current_user: ClientUser,
    service: ClientPostServiceDep,
):
    return service.get_my_posts(current_user.id)


@router.get(
    "/posts/{post_id}",
    dependencies=[Depends(get_current_user)],
)

def get_post(
    post_id: int,
    service: ClientPostServiceDep,
):
    return service.get_post(post_id)    


@router.get(
    "/{client_id}/posts",
    dependencies=[Depends(get_current_user)],
)

def get_client_posts(
    client_id: int,
    service: ClientPostServiceDep,
):
    return service.get_client_posts(client_id)


@router.patch(
    "/posts/{post_id}",
    response_model=ClientPostResponse,
)
def update_post(
    post_id: int,
    data: ClientPostUpdate,
    current_user: ClientUser,
    service: ClientPostServiceDep,
):
    return service.update_post(current_user.id, post_id, data)


@router.delete(
    "/posts/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_post(
    post_id: int,
    current_user: ClientUser,
    service: ClientPostServiceDep,
):
    service.delete_post(current_user.id, post_id)
