from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, SmallInteger, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.features.client_profiles.model import ClientProfile
    from app.features.tutor_profiles.model import TutorProfile


class TutorReview(TimestampMixin, Base):
    __tablename__ = "tutor_reviews"
    __table_args__ = (
        CheckConstraint(
            "rating BETWEEN 1 AND 5",
            name="ck_tutor_reviews_rating_range",
        ),
        UniqueConstraint(
            "client_id",
            "tutor_id",
            name="uq_tutor_reviews_client_id_tutor_id",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(
        ForeignKey("client_profiles.id", ondelete="CASCADE"),
        index=True,
    )
    tutor_id: Mapped[int] = mapped_column(
        ForeignKey("tutor_profiles.id", ondelete="CASCADE"),
        index=True,
    )
    rating: Mapped[int] = mapped_column(SmallInteger)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    client: Mapped["ClientProfile"] = relationship()
    tutor: Mapped["TutorProfile"] = relationship()
