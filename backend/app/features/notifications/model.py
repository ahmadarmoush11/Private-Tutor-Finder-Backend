import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Index, false, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.features.client_posts.model import ClientPost
    from app.features.lesson_requests.model import LessonRequest
    from app.features.users.model import User


class NotificationType(str, enum.Enum):
    TUTOR_AVAILABLE = "tutor_available"
    LESSON_REQUEST_RECEIVED = "lesson_request_received"
    LESSON_REQUEST_ACCEPTED = "lesson_request_accepted"
    LESSON_REQUEST_REJECTED = "lesson_request_rejected"
    LESSON_REQUEST_CONFIRMED = "lesson_request_confirmed"


class Notification(Base):
    __tablename__ = "notifications"
    __table_args__ = (
        Index("ix_notifications_recipient_id_created_at", "recipient_id", "created_at"),
        Index(
            "ix_notifications_recipient_id_unread",
            "recipient_id",
            postgresql_where="is_read = false",
            sqlite_where="is_read = 0",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    recipient_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    actor_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    type: Mapped[NotificationType] = mapped_column(
        Enum(
            NotificationType,
            name="notification_type",
            values_callable=lambda e: [member.value for member in e],
        ),
    )
    lesson_request_id: Mapped[int | None] = mapped_column(
        ForeignKey("lesson_requests.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    client_post_id: Mapped[int | None] = mapped_column(
        ForeignKey("client_posts.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    is_read: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=false(),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    recipient: Mapped["User"] = relationship(foreign_keys=[recipient_id])
    actor: Mapped["User | None"] = relationship(foreign_keys=[actor_id])
    lesson_request: Mapped["LessonRequest | None"] = relationship()
    client_post: Mapped["ClientPost | None"] = relationship()
