from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin
from app.shared.dates import calculate_age

if TYPE_CHECKING:
    from app.features.client_posts.model import ClientPost
    from app.features.lesson_requests.model import LessonRequest
    from app.features.users.model import User


class ClientProfile(TimestampMixin, Base):
    __tablename__ = "client_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True,
    )
    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)

    user: Mapped["User"] = relationship(back_populates="client_profile")
    posts: Mapped[list["ClientPost"]] = relationship(
        back_populates="client",
        cascade="all, delete-orphan",
    )
    lesson_requests: Mapped[list["LessonRequest"]] = relationship(
        back_populates="client",
        cascade="all, delete-orphan",
    )

    @property
    def age(self) -> int | None:
        if self.date_of_birth is None:
            return None
        return calculate_age(self.date_of_birth)
