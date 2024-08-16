from ast import Str
from decimal import Decimal
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field, Strict, StrictInt, ValidationError

print("\n--- Data coercion: lax mode ---")
# https://docs.pydantic.dev/latest/concepts/conversion_table/
# pydantic's default mode is lax mode where data can be coerced into a different type
class MyModel(BaseModel):
    my_int: int
    my_str: str

external_data = {"my_int": "123", "my_str": "abc"}
my_model = MyModel(**external_data)

print(type(my_model.my_int))  # <class 'int'>

class MyModel(BaseModel):
    my_number: Decimal
    my_str: str

external_data = {"my_number": 12.35, "my_str": "abc"}
my_model = MyModel(**external_data)

print(type(my_model.my_number))  # <class 'decimal.Decimal'>

print("\n--- Field strict mode ---")
# the strict parameter specifies whether the field should be validated in strict mode

class MyModel(BaseModel):
    my_int: int = Field(strict=True)
    my_str: str

external_data = {"my_int": "123", "my_str": "abc"}
try:
    my_model =MyModel(**external_data)
except ValidationError as e:
    print(e.errors())

class MyModel(BaseModel):
    my_int: Annotated[int, Field(strict=True)]
    my_str: str

external_data = {"my_int": "123", "my_str": "abc"}
try:
    my_model =MyModel(**external_data)
except ValidationError as e:
    print(e.errors())

class MyModel(BaseModel):
    my_int: Annotated[int, Strict()]
    my_str: str

external_data = {"my_int": "123", "my_str": "abc"}
try:
    my_model =MyModel(**external_data)
except ValidationError as e:
    print(e.errors())

print("\n--- Strict Types ---")
# https://docs.pydantic.dev/latest/api/types/#pydantic.types

class MyModel(BaseModel):
    my_int: StrictInt
    my_str: str

external_data = {"my_int": "123", "my_str": "abc"}
try:
    my_model =MyModel(**external_data)
except ValidationError as e:
    print(e.errors())  # Input should be a valid integer

print("\n--- Config strict mode---")
class MyModel(BaseModel):
    model_config = ConfigDict(strict=True)

    my_int: int 
    my_str: str

external_data = {"my_int": "123", "my_str": b"abc"}
try:
    my_model =MyModel(**external_data)
except ValidationError as e:
    print(e.errors())

print("\n--- Validation strict mode---")
class MyModel(BaseModel):

    my_int: int 
    my_str: str

external_data = {"my_int": "123", "my_str": b"abc"}
try:
    my_model =MyModel.model_validate(external_data, strict=True)
except ValidationError as e:
    print(e.errors())

