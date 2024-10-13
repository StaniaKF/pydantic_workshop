from pydantic import BaseModel, ValidationError, field_validator
import pprint

# DOCUMENTATION: https://docs.pydantic.dev/2.9/concepts/validators/#reusing-validators

class MyModel(BaseModel):
    my_int: int 
    my_str: str

    @field_validator("my_int", mode="after")
    @classmethod
    def validate_even_number(cls, value: int) -> int:    
        if value % 2 != 0:
            raise ValueError("Must be an even number")
        return value

def validate_even_number(value: int) -> int:    
    if value % 2 != 0:
        raise ValueError("Must be an even number")
    return value

class MyModel(BaseModel):
    my_int: int 
    my_str: str

    validate_int = field_validator("my_int", mode="after")(validate_even_number)

external_data = {"my_int": 123, "my_str": "abc"}

try:
    my_model =MyModel(**external_data)
except ValidationError as e:
    pprint.pp(e.errors())