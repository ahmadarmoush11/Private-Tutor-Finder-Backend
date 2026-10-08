import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.db.models import User, UserRole


logger = logging.getLogger(__name__)

SEED_PASSWORD = "ahmad200317@"

SEED_USERS = [
    {
        "first_name": "Admin",
        "last_name": "User",
        "email": "admin@tutorfinder.com",
        "role": UserRole.ADMIN,
    },
    {
        "first_name": "Client",
        "last_name": "User",
        "email": "client@tutorfinder.com",
        "role": UserRole.CLIENT,
    },
    {
        "first_name": "Tutor",
        "last_name": "User",
        "email": "tutor@tutorfinder.com",
        "role": UserRole.TUTOR,
    },
]


def seed_users(db: Session) -> int:
    emails = [user["email"] for user in SEED_USERS]
    existing_emails = set(db.scalars(select(User.email).where(User.email.in_(emails))))
    missing_users = [user for user in SEED_USERS if user["email"] not in existing_emails]

    if not missing_users:
        return 0

    password_hash = hash_password(SEED_PASSWORD)
    db.add_all(User(**user, password_hash=password_hash) for user in missing_users)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return 0

    logger.info("Seeded %d users", len(missing_users))
    return len(missing_users)


if __name__ == "__main__":
    with SessionLocal() as session:
        added = seed_users(session)
        print(f"Added {added} users")
