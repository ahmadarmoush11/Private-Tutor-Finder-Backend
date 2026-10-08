from sqlalchemy.orm import Session
from app.features.client_posts.model import ClientPost

class ClientPostRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_post(
        self,
        post: ClientPost,
    ):
        self.db.add(post)
        self.db.flush()
        self.db.refresh(post)
        return post

    def get_post_by_id(
        self,
        post_id: int,
    ):
        return(
            self.db.query(ClientPost)
            .filter(ClientPost.id==post_id)
            .first()
        )

    def update(
        self,
        post: ClientPost,
        values: dict,
    ) -> ClientPost:
        for field, value in values.items():
            setattr(post, field, value)
        self.db.flush()
        self.db.refresh(post)
        return post

    def delete(
        self,
        post: ClientPost,
    ) -> None:
        self.db.delete(post)
        self.db.flush()

    def get_client_posts(
        self,
        client_id: int,
    ):
        return(
            self.db.query(ClientPost)
            .filter(ClientPost.client_id==client_id)
            .all()
        )


