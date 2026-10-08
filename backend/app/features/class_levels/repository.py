from sqlalchemy.orm import Session

from app.features.class_levels.model import ClassLevel


class ClassLevelRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, class_level_id: int) -> ClassLevel | None:
        return self.db.get(ClassLevel, class_level_id)
