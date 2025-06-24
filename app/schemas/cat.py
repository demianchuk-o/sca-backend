# app/schemas/cat.py
from pydantic import BaseModel, ConfigDict, validator

class CatBase(BaseModel):
    name: str
    years_of_experience: int
    breed: str
    salary: float

    @validator("years_of_experience")
    def validate_years_of_experience(cls, value):
        if value < 0:
            raise ValueError("Years of experience must be non-negative")
        return value

    @validator("salary")
    def validate_salary(cls, value):
        if value < 0:
            raise ValueError("Salary must be non-negative")
        return value


class CatCreate(CatBase):
    pass


class CatUpdate(BaseModel):
    salary: float

    @validator("salary")
    def validate_salary(cls, value):
        if value < 0:
            raise ValueError("Salary must be non-negative")
        return value


class Cat(CatBase):
    id: int

    model_config = ConfigDict(from_attributes=True)