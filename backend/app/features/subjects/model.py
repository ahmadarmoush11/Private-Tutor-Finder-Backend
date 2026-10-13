from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.features.client_posts.model import ClientPost
    from app.features.tutor_posts.model import TutorPost


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    client_posts: Mapped[list["ClientPost"]] = relationship(
        secondary="client_post_subjects",
        back_populates="subjects",
    )
    tutor_posts: Mapped[list["TutorPost"]] = relationship(
        secondary="tutor_post_subjects",
        back_populates="subjects",
    )

    def __repr__(self) -> str:
        return f"<Subject id={self.id} name={self.name!r}>"
