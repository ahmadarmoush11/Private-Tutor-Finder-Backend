from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class ClientProfile(TimestampMixin, Base):
    __tablename__ = "client_profiles"
    __table_args__ = (
        CheckConstraint("grade BETWEEN 1 AND 12", name="ck_client_profiles_grade_range"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True,
    )
    grade: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    school: Mapped[str | None] = mapped_column(String(150), nullable=True)
    location: Mapped[str | None] = mapped_column(String(150), nullable=True)

    user: Mapped["User"] = relationship(back_populates="client_profile")
