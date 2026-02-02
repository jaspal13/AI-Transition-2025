from pydantic import BaseModel, Field, ValidationError, ConfigDict, field_validator

class Person(BaseModel):
    name: str = Field(..., min_length=1) #this means name is a string and Field(...) makes it mandatory with min lenght as 1
    age: int

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        value = value.strip() # to not allow '' type names
        if not value:
            raise ValueError("name cannot be empty")
        return value.title()

    @field_validator("age")
    @classmethod
    def validate_age(cls, value: int) -> int:
        if value < 18:
            raise ValueError("age must be >= 18")
        return value

    model_config = ConfigDict(frozen=True) #immutable