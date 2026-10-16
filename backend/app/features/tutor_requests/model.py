from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin
from app.shared.enums import RequestStatus

if TYPE_CHECKING:
    from app.features.client_posts.model import ClientPost
    from app.features.tutor_profiles.model import TutorProfile


class TutorRequest(TimestampMixin, Base):
    __tablename__ = "tutor_requests"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tutor_id: Mapped[int] = mapped_column(
        ForeignKey("tutor_profiles.id", ondelete="CASCADE"),
        index=True,
    )
    client_post_id: Mapped[int] = mapped_column(
        ForeignKey("client_posts.id", ondelete="CASCADE"),
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

    tutor: Mapped["TutorProfile"] = relationship(back_populates="requests")
    client_post: Mapped["ClientPost"] = relationship(back_populates="requests")
