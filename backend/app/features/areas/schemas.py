from pydantic import BaseModel, ConfigDict


class AreaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    district: str
    governorate: str


class DistrictOut(BaseModel):
    name: str
    governorate: str
