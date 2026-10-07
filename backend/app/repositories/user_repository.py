from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import EmailAlreadyRegisteredError
from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        return self.db.scalar(select(User).where(User.email == email.strip().lower()))

    def create(self, user: User) -> User:
        self.db.add(user)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise EmailAlreadyRegisteredError()
        self.db.refresh(user)
        return user
