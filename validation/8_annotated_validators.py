import json
import pprint
from typing import TypeAliasType
from pydantic import BaseModel, BeforeValidator, PlainValidator, ValidationError, ValidationInfo, field_validator
from typing_extensions import Annotated
from pydantic.functional_validators import AfterValidator

print("--- Annotated validators ---")
# # DOCUMENTATION: https://docs.pydantic.dev/2.9/concepts/validators/#annotated-validators
# Annotated validators should be used whenever you want to bind validation to a type instead of a model or a field

class MyModel(BaseModel):
    my_int: int 
    my_str_1: str   
    my_str_2: str

    @field_validator("my_str_1", "my_str_2")
    @classmethod
    def validate_alphanumeric(cls, value: str) -> str:
        if not value.isalnum():
            raise ValueError("Must be alphanumeric")
        return value.title()


class MyModel(BaseModel):
    my_strs: list[str] 

def validate_alphanumeric(value: str) -> str:
    assert value.isalnum(), "Must be alphanumeric"  # here we use assert instead of raising ValueError
    return value

def capitalize(value: str) -> str:
    return value.title()

AlphanumericStr = Annotated[str, AfterValidator(validate_alphanumeric), AfterValidator(capitalize)]

class MyModel(BaseModel):
    my_strs: list[AlphanumericStr] 

external_data = {"my_strs": ["ghi", "jkl"]}
print(MyModel(**external_data))  # my_strs=['Ghi', 'Jkl']

external_data = {"my_strs": ["gh!i", "jk?l"]}
try:
    MyModel(**external_data)
except ValidationError as e:
    pprint.pp(e.errors())

class MyModel(BaseModel):
    my_strs: list[AlphanumericStr] 
    my_another_str: AlphanumericStr


AlphanumericStrType = TypeAliasType('AlphanumericStrType', Annotated[str, AfterValidator(validate_alphanumeric), AfterValidator(capitalize)])
type AlphanumericStrType2 = Annotated[str, AfterValidator(validate_alphanumeric), AfterValidator(capitalize)]

class MyModel(BaseModel):
    my_strs: list[AlphanumericStrType2] 

external_data = {"my_strs": ["ghi", "jkl"]}
print(MyModel(**external_data)) # my_strs=['Ghi', 'Jkl']



