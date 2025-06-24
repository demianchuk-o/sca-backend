from pydantic import BaseModel, ConfigDict

class TargetBase(BaseModel):
    name: str
    country: str

class TargetCreate(TargetBase):
    pass

class TargetUpdate(BaseModel):
    notes: str | None = None
    complete: bool | None = None

class Target(TargetBase):
    id: int
    notes: str | None
    complete: bool

    model_config = ConfigDict(from_attributes=True)