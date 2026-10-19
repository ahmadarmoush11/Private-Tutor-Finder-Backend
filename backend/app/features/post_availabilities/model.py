from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.features.client_posts.model import ClientPost
    from app.features.tutor_profiles.model import TutorProfile


class PostAvailability(TimestampMixin, Base):
    __tablename__ = "post_availabilities"
    __table_args__ = (
        UniqueConstraint(
            "tutor_id",
            "client_post_id",
            name="uq_post_availabilities_tutor_id_client_post_id",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tutor_id: Mapped[int] = mapped_column(
        ForeignKey("tutor_profiles.id", ondelete="CASCADE"),
        index=True,
    )
    client_post_id: Mapped[int] = mapped_column(
        ForeignKey("client_posts.id", ondelete="CASCADE"),
        index=True,
    )

    tutor: Mapped["TutorProfile"] = relationship(back_populates="post_availabilities")
    client_post: Mapped["ClientPost"] = relationship(back_populates="availabilities")
