from pydantic import BaseModel, ConfigDict, field_validator
from .target import Target, TargetCreate
from .cat import Cat

class MissionBase(BaseModel):
    pass

class MissionCreate(MissionBase):
    targets: list[TargetCreate]

    @field_validator("targets")
    def validate_targets_count(cls, v):
        if not 1 <= len(v) <= 3:
            raise ValueError("A mission must have between 1 and 3 targets.")
        return v

class Mission(MissionBase):
    id: int
    complete: bool
    cat: Cat | None = None
    targets: list[Target] = []

    model_config = ConfigDict(from_attributes=True)