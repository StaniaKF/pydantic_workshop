import pprint
from pydantic import BaseModel, Field, ValidationError, field_validator


print("--- Field validator ---")

class MyModel(BaseModel):
    my_int: int # = Field(multiple_of=2)
    my_str_1: str
    my_str_2: str

    @field_validator("my_int")
    @classmethod
    def validate_even_number(cls, value: int) -> int:
        if value % 2 != 0:
            raise ValueError("Value must be an even number")
        return value
    

external_data = {"my_int": 123, "my_str_1": "abc", "my_str_2": "def"}
try:
    my_model =MyModel(**external_data)
except ValidationError as e:
    pprint.pp(e.errors())   


class MyModel(BaseModel):
    my_int: int 
    my_str_1: str
    my_str_2: str

    @field_validator("my_str_1", "my_str_2")  # *
    @classmethod
    def validate_alphanumeric(cls, value: str) -> str:
        if not value.isalnum():
            raise ValueError("Must be alphanumeric")
        return value

external_data = {"my_int": 123, "my_str_1": "ab*c", "my_str_2": "de?f"}
try:
    my_model =MyModel(**external_data)
except ValidationError as e:
    pprint.pp(e.errors())


class MyModel(BaseModel):
    my_int: int 
    my_str_1: str
    my_str_2: str

    @field_validator("my_str_1", "my_str_2")  # *
    @classmethod
    def validate_alphanumeric(cls, value: str) -> str:
        if not value.isalnum():
            raise ValueError("Must be alphanumeric")
        #return value

external_data = {"my_int": 123, "my_str_1": "abc", "my_str_2": "def"}
print(MyModel(**external_data))  # my_int=123 my_str_1=None my_str_2=None


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
    
external_data = {"my_int": 123, "my_str_1": "abc", "my_str_2": "def"}
print(MyModel(**external_data))  # my_int=123 my_str_1='Abc' my_str_2='Def'

print("\n--- Field validator default value validation ---")

class MyModel(BaseModel):
    my_int: int 
    my_str_1: str = "hello"
    my_str_2: str

    @field_validator("my_str_1", "my_str_2") 
    @classmethod
    def validate_alphanumeric(cls, value: str) -> str:
        if not value.isalnum():
            raise ValueError("Must be alphanumeric")
        return value.title()
    
external_data = {"my_int": 123, "my_str_2": "def"}
print(MyModel(**external_data)) # my_int=123 my_str_1='hello' my_str_2='Def'


class MyModel(BaseModel):
    my_int: int 
    my_str_1: str = Field(default="hello", validate_default=True)
    my_str_2: str

    @field_validator("my_str_1", "my_str_2") 
    @classmethod
    def validate_alphanumeric(cls, value: str) -> str:
        if not value.isalnum():
            raise ValueError("Must be alphanumeric")
        return value.title()
    
external_data = {"my_int": 123, "my_str_2": "def"}
print(MyModel(**external_data))  # my_int=123 my_str_1='Hello' my_str_2='Def'


