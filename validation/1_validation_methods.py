import pprint
from pydantic import BaseModel, ValidationError
import json

class MyModel(BaseModel):
    my_int: int 
    my_str: str

my_model = MyModel(my_int=123, my_str="abc")
print(my_model)

external_data = {"my_int": 123, "my_str": "abc"}
my_model = MyModel(**external_data)
print(my_model)

print("\n--- model_validate ---")
# parameters: obj, strict, from_attribute, context
my_model = MyModel.model_validate(external_data)
print(my_model)


class ModelA(BaseModel):
    my_str: str

class ModelB(BaseModel):
    my_str: str
    my_int: int

model_b = ModelB(my_str="abc", my_int=20)

model_b_2 = ModelB.model_validate(model_b)

try:
    model_a = ModelA.model_validate(model_b)
except ValidationError as e:
    pprint.pp(e.errors())

model_a = ModelA.model_validate(model_b, from_attributes=True)
print(model_a)

print("\n--- model_validate_json ---")
json_data = json.dumps(external_data)
my_model = MyModel.model_validate_json(json_data)
print(my_model)