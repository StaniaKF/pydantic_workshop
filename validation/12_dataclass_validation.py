import pprint
from pydantic import BaseModel, ValidationError, field_validator
from pydantic.dataclasses import dataclass

class MyModel(BaseModel):
    my_str_1: str   
    my_str_2: str

    @field_validator("my_str_1", "my_str_2")
    @classmethod
    def validate_alphanumeric(cls, value: str) -> str:
        if not value.isalnum():
            raise ValueError("Must be alphanumeric")
        return value

external_data = {"my_str_1": "ab_c", "my_str_2": "def"}
try:
    my_model =MyModel(**external_data)
except ValidationError as e:
    pprint.pp(e.errors())

# dataclass needs to be imported from pydantic and not the dataclasses package

@dataclass
class MyModel:
    my_str_1: str   
    my_str_2: str

    @field_validator("my_str_1", "my_str_2")
    @classmethod
    def validate_alphanumeric(cls, value: str) -> str:
        if not value.isalnum():
            raise ValueError("Must be alphanumeric")
        return value

external_data = {"my_str_1": "ab_c", "my_str_2": "def"}
try:
    my_model =MyModel(**external_data)
except ValidationError as e:
    pprint.pp(e.errors())

# Pydantic dataclasses are not a replacement for Pydantic models. 
# They provide a similar functionality to stdlib dataclasses with the addition of Pydantic validation.
# There are cases where subclassing using Pydantic models is the better choice.
# https://docs.pydantic.dev/latest/concepts/dataclasses/