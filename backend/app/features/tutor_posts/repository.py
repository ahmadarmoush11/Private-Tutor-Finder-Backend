from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.features.tutor_posts.model import TutorPost


class TutorPostRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, post_id: int) -> TutorPost | None:
        return self.db.scalar(
            select(TutorPost)
            .options(selectinload(TutorPost.class_levels))
            .where(TutorPost.id == post_id)
        )

    def get_by_tutor_id(self, tutor_id: int) -> list[TutorPost]:
        return list(
            self.db.scalars(
                select(TutorPost)
                .options(selectinload(TutorPost.class_levels))
                .where(TutorPost.tutor_id == tutor_id)
                .order_by(TutorPost.created_at.desc(), TutorPost.id.desc())
            )
        )

    def create(self, post: TutorPost) -> TutorPost:
        self.db.add(post)
        self.db.flush()
        self.db.refresh(post)
        return post

    def update(self, post: TutorPost, values: dict) -> TutorPost:
        for field, value in values.items():
            setattr(post, field, value)
        self.db.flush()
        self.db.refresh(post)
        return post

    def delete(self, post: TutorPost) -> None:
        self.db.delete(post)
        self.db.flush()
