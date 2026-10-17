from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin
from app.shared.enums import RequestStatus

if TYPE_CHECKING:
    from app.features.client_profiles.model import ClientProfile
    from app.features.tutor_posts.model import TutorPost


class LessonRequest(TimestampMixin, Base):
    __tablename__ = "lesson_requests"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(
        ForeignKey("client_profiles.id", ondelete="CASCADE"),
        index=True,
    )
    tutor_post_id: Mapped[int] = mapped_column(
        ForeignKey("tutor_posts.id", ondelete="CASCADE"),
        index=True,
    )
    status: Mapped[RequestStatus] = mapped_column(
        Enum(
            RequestStatus,
            name="request_status",
            values_callable=lambda e: [member.value for member in e],
        ),
        default=RequestStatus.PENDING,
        server_default=RequestStatus.PENDING.value,
        index=True,
    )

    client: Mapped["ClientProfile"] = relationship(back_populates="lesson_requests")
    tutor_post: Mapped["TutorPost"] = relationship(back_populates="lesson_requests")
