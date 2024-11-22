from typing import Any, Self
from pydantic import BaseModel, ValidationError, model_validator

# DOCUMENTATION: https://docs.pydantic.dev/latest/concepts/validators/#model-validators
print("--- Model validators ---")
# model validators can be used to validate the whole model or when you need to compare multiple fields
# model validators can be used in three modes: before, after and wrap

external_data = {"number": "323", "decimal": "45", "my_float_2": "235"}

class MyModel(BaseModel):
    my_float_1: float
    my_float_2: float

    @model_validator(mode="before")
    @classmethod
    def create_my_float_1(cls, data: Any) -> Any:
        if isinstance(data, dict) and isinstance(data.get("number"), str) and isinstance(data.get("decimal"), str):
            data["my_float_1"] = f"{data['number']}.{data['decimal']}"
        return data

print(MyModel(**external_data)) # my_float_1=323.45 my_float_2=235.0


class MyModel(BaseModel):
    my_float_1: float
    my_float_2: float

    @model_validator(mode="before")
    @classmethod
    def create_my_float_1(cls, data: Any) -> Any:
        if isinstance(data, dict) and isinstance(data.get("number"), str) and isinstance(data.get("decimal"), str):
            data["my_float_1"] = f"{data['number']}.{data['decimal']}"
        return data
    
    @model_validator(mode="after")
    def validate_floats(self) -> Self:
        if self.my_float_1 <= self.my_float_2:
            raise ValueError("my_float_1 must be larger than my_float_2")
        return self

valid_external_data = {"number": "323", "decimal": "45", "my_float_2": "235"}
print(MyModel(**valid_external_data)) 

invalid_external_data = {"number": "123", "decimal": "45", "my_float_2": "235"}
try:
    MyModel(**invalid_external_data)
except ValidationError as e:
    print(e.errors()) # 'msg': 'Value error, my_float_1 must be larger than my_float_2'

