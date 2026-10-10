from pydantic import BaseModel, ConfigDict

from app.features.class_levels.model import EducationLevel


class ClassLevelOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    level: EducationLevel
