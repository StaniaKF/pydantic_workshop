import pprint
from pydantic import BaseModel, ValidationError, ValidationInfo, field_validator


class MyModel(BaseModel):
    my_str_1: str 
    my_str_2: str

    @field_validator("my_str_1", "my_str_2") 
    @classmethod
    def validate_alphanumeric(cls, value: str, info: ValidationInfo) -> str:
        if not value.isalnum():
            raise ValueError(f"{info.field_name} must be alphanumeric")
        return value.title()

external_data = {"my_str_1": "ab-c", "my_str_2": "de-f"}
try:
    MyModel(**external_data)
except ValidationError as e:
    pprint.pp(e.errors())

print("\n--- ValidationInfo data attribute ---")

class MyModel(BaseModel):
    my_str_1: str 
    my_str_2: str

    @field_validator("my_str_1", "my_str_2") 
    @classmethod
    def validate_alphanumeric(cls, value: str, info: ValidationInfo) -> str:
        if not value.isalnum():
            raise ValueError(f"{info.field_name} must be alphanumeric")
        return value.title()

external_data = {"my_str_1": "abc", "my_str_2": "def"}
MyModel(**external_data)

class MyModel(BaseModel):
    my_str_1: str 
    my_str_2: str

    @field_validator("my_str_2")
    @classmethod    
    def str_2_the_same_length_as_str_1(cls, value: str, info: ValidationInfo) -> str: 
        if len(value) != len(info.data["my_str_1"]):
            raise ValueError(f"{info.field_name} must be the same length as my_str_1")
        return value
    
external_data = {"my_str_1": "abd", "my_str_2": "defg"}
try:
    MyModel(**external_data)
except ValidationError as e:
    pprint.pp(e.errors())


external_data = {"my_str_1": 123, "my_str_2": "defg"}
# MyModel(**external_data)