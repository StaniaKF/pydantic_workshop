import pprint
from pydantic import BaseModel, ValidationError, ValidationInfo, field_validator

# context can be useful when you need to provide additional information which is
# necessary for validation dynamically at run time

dynamic_values = ["a", "b", "c"]

class MyModel(BaseModel):
    my_str: str

    @field_validator("my_str")
    @classmethod
    def validate_my_str_has_correct_value(cls, value: str) -> str:
        if value not in dynamic_values:
            raise ValueError(f"{value} is not in {dynamic_values}")
        return value

try:
    MyModel(my_str="d")
except ValidationError as e:
    pprint.pp(e.errors())


class MyModel(BaseModel):
    my_str: str

    @field_validator("my_str")
    @classmethod
    def validate_my_str_has_correct_value(cls, value: str, info: ValidationInfo) -> str:
        dynamic_values_in_context = info.context["dynamic_values"]
        if value not in dynamic_values_in_context:
            raise ValueError(f"{value} is not in {dynamic_values_in_context}")
        return value

try:
    MyModel.model_validate({"my_str": 'd'}, context={"dynamic_values": dynamic_values})
except ValidationError as e:
    pprint.pp(e.errors())