import pprint
from pydantic import BaseModel, ValidationError
### Pydantic models define fields as annotated attributes

print("--- Basic model usage ---")

class MyModel(BaseModel):
    my_int: int
    my_str: str 

MyModel(my_int=1, my_str='foo')
external_data = {'my_int': 123, 'my_str': 'bar'}
my_model = MyModel(**external_data)
print(my_model)

external_data = {"my_int": "abs", "my_str": 123}
try:
    my_model = MyModel(**external_data)
except ValidationError as e:
    pprint.pp(e.errors())

### validation = process of instantiating a model that adheres to specified types and constraints

print("\n--- Data coercion ---")
### coercion = process of converting data from one data type to another

external_data = {"my_int": "123", "my_str": "bar"}
my_model = MyModel(**external_data)
print(type(my_model.my_int))  # <class 'int'>

# https://docs.pydantic.dev/latest/concepts/models/#model-methods-and-properties

print("\n--- model_validate ---")
my_model = MyModel(**external_data)
print(my_model)
my_model_2 = MyModel.model_validate(external_data)
print(my_model_2)

print("\n--- Nested models ---")
class MyModel(BaseModel):
    my_int: int
    my_str: str 

class TopModel(BaseModel):
    my_model: MyModel

print(TopModel(my_model=MyModel(**external_data)))
