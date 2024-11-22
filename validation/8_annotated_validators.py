import json
import pprint
from typing import Any, TypeAliasType
from pydantic import BaseModel, BeforeValidator, PlainValidator, ValidationError, ValidationInfo, ValidatorFunctionWrapHandler, WrapValidator, field_validator
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
# print(MyModel(**external_data)) # my_strs=['Ghi', 'Jkl']


# validation modes:
# after: run after pydantic's internal parsing. 
# they are generally more type safe and easier to implement

# before: run before pydantic's internal parsing and validation.
# flexible - can modify the raw input 
# but they also have to deal with the raw input - which could by any arbitrary object

# plain: like before but terminate validation immediately
# pydantic does not do any of its internal validation

# wrap: the most flexible
# can run before or after pydantic and other validators do their thing 
# or they can terminate validation immediately both with a successful value or an error

print("\n--- Annotated Wrap mode ---")

def validate_int(value: Any, handler: ValidatorFunctionWrapHandler) -> int:
    try:
        return handler(value) # let pyndantic do its thing
    except ValidationError:
        return 0
    
type MyInt = Annotated[int, WrapValidator(validate_int)] 

class MyModel(BaseModel):
    my_int: MyInt

external_data = {"my_int": "hello"}
print(MyModel(**external_data)) # my_int=0
external_data = {"my_int": 123}
print(MyModel(**external_data)) # my_int=123


def validate_int(value: Any, handler: ValidatorFunctionWrapHandler, info: ValidationInfo) -> int:
    if info.mode == "json":
        assert isinstance(value, str), "Must be a string"
    try:
        return handler(value) # let pyndantic do its thing
    except ValidationError:
        return 0
    
type MyInt = Annotated[int, WrapValidator(validate_int)] 

class MyModel(BaseModel):
    my_int: MyInt

external_data = {"my_int": "hello"}
print(MyModel(**external_data)) # my_int=0
external_data = {"my_int": 123}
print(MyModel(**external_data)) # my_int=123

json_data = json.dumps({"my_int": 123})
try:
    MyModel.model_validate_json(json_data)
except ValidationError as e:
    print(e.errors())

json_data = json.dumps({"my_int": "123"})
print(MyModel.model_validate_json(json_data)) 


print("\n--- Ordering of validators ---")

def before_validator_1(value: int) -> int:
    print("before-1")
    return value

def before_validator_2(value: int) -> int:
    print("before-2")
    return value

def after_validator_1(value: int) -> int:
    print("after-1")
    return value

def after_validator_2(value: int) -> int:
    print("after-2")
    return value

type MyInt = Annotated[
    int, 
    BeforeValidator(before_validator_1), 
    BeforeValidator(before_validator_2), 
    AfterValidator(after_validator_1), 
    AfterValidator(after_validator_2)
]

class MyModel(BaseModel):
    my_int: MyInt

MyModel(my_int=123)

# before-2
# before-1
# after-1
# after-2

def wrap_validator_1(value: int, handler: ValidatorFunctionWrapHandler) -> int:
    print("wrap-1: pre")
    result =  handler(value)
    print("wrap-1: post")
    return result

def wrap_validator_2(value: int, handler: ValidatorFunctionWrapHandler) -> int:
    print("wrap-2: pre")
    result =  handler(value)
    print("wrap-2: post")
    return result

MyInt = Annotated[
    int, 
    BeforeValidator(before_validator_1), 
    BeforeValidator(before_validator_2), 
    AfterValidator(after_validator_1), 
    AfterValidator(after_validator_2),
    WrapValidator(wrap_validator_1),
    WrapValidator(wrap_validator_2)
]

class MyModel(BaseModel):
    my_int: MyInt

print("\n")
MyModel(my_int=123)

# wrap-2: pre
# wrap-1: pre
# before-2
# before-1
# after-1
# after-2
# wrap-1: post
# wrap-2: post

