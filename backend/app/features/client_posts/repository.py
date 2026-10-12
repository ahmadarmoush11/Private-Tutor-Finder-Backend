from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.features.client_posts.model import ClientPost


class ClientPostRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, post_id: int) -> ClientPost | None:
        return self.db.scalar(
            select(ClientPost)
            .options(selectinload(ClientPost.class_level))
            .where(ClientPost.id == post_id)
        )

    def get_by_client_id(self, client_id: int) -> list[ClientPost]:
        return list(
            self.db.scalars(
                select(ClientPost)
                .options(selectinload(ClientPost.class_level))
                .where(ClientPost.client_id == client_id)
                .order_by(ClientPost.created_at.desc(), ClientPost.id.desc())
            )
        )

    def create(self, post: ClientPost) -> ClientPost:
        self.db.add(post)
        self.db.flush()
        self.db.refresh(post)
        return post

    def update(self, post: ClientPost, values: dict) -> ClientPost:
        for field, value in values.items():
            setattr(post, field, value)
        self.db.flush()
        self.db.refresh(post)
        return post

    def delete(self, post: ClientPost) -> None:
        self.db.delete(post)
        self.db.flush()
