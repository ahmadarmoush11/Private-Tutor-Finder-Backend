from app.db.seeds.class_levels import seed_class_levels
from app.db.seeds.users import seed_users
from app.db.session import SessionLocal


def run_seeds() -> None:
    with SessionLocal() as db:
        seed_class_levels(db)
        seed_users(db)


if __name__ == "__main__":
    run_seeds()
