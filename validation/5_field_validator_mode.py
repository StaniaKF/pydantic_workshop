#  mode = before, after and plain

import numbers
import pprint
from typing import Any
from pydantic import BaseModel, ValidationError, field_validator


print("--- Mode after ---")

class MyModel(BaseModel):
    my_int: int 
    my_str: str

    @field_validator("my_int")
    @classmethod
    def validate_even_number(cls, value: int) -> int:    
        if value % 2 != 0:
            raise ValueError("Must be an even number")
        return value

external_data = {"my_int": 123, "my_str": "abc"}
try:
    my_model =MyModel(**external_data)
except ValidationError as e:
    pprint.pp(e.errors())


class MyModel(BaseModel):
    my_int: int 
    my_str: str

    @field_validator("my_int", mode="after")
    @classmethod
    def validate_even_number(cls, value: int) -> int:    
        if value % 2 != 0:
            raise ValueError("Must be an even number")
        return value

external_data = {"my_int": "123", "my_str": "abc"}
try:
    my_model =MyModel(**external_data)
except ValidationError as e:
    pprint.pp(e.errors())

print("\n--- Mode before ---")

class MyModel(BaseModel):
    my_int: int 
    my_str: str

    @field_validator("my_int", mode="before")
    @classmethod
    def validate_even_number(cls, value: int) -> int:    
        if value % 2 != 0:
            raise ValueError("Must be an even number")
        return value

external_data = {"my_int": "123", "my_str": "abc"}
try:
    my_model =MyModel(**external_data)
except TypeError as e:
    pprint.pp(e)  # TypeError('not all arguments converted during string formatting')


class MyModel(BaseModel):
    my_int: int 
    my_str: str

external_data = {"my_int": 123.23, "my_str": "abc"}

try:
    my_model =MyModel(**external_data)
except ValidationError as e:
    pprint.pp(e.errors())


class MyModel(BaseModel):
    my_int: int 
    my_str: str

    @field_validator("my_int", mode="before")
    @classmethod
    def convert_float_into_int(cls, value: Any) -> int | Any:
        if isinstance(value, numbers.Number):
            return int(value)
        return value

external_data = {"my_int": 123.456, "my_str": "abc"}

print(MyModel(**external_data)) # my_int=123 my_str='abc'

external_data = {"my_int": "123.456", "my_str": "abc"}
try:
    my_model =MyModel(**external_data)
except ValidationError as e:
    pprint.pp(e.errors())
    



