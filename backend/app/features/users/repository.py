from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.features.users.exceptions import (
    EmailAlreadyRegisteredError,
    UsernameAlreadyTakenError,
)
from app.features.users.model import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        return self.db.scalar(select(User).where(User.email == email.strip().lower()))

    def get_by_username(self, username: str) -> User | None:
        return self.db.scalar(
            select(User).where(User.username == username.strip().lower())
        )

    def create(self, user: User) -> User:
        self.db.add(user)
        try:
            self.db.flush()
        except IntegrityError as error:
            if "username" in str(error.orig).lower():
                raise UsernameAlreadyTakenError()
            raise EmailAlreadyRegisteredError()
        self.db.refresh(user)
        return user
