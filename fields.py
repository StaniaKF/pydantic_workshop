
import pprint
from typing import Optional
from pydantic import BaseModel, Field, ValidationError
from uuid import uuid4

print("--- Optional fields ---")

class MyModel(BaseModel):
    my_int: int
    my_str: str | None = None
    #my_str: Optional[str] = None

print(MyModel(my_int=123))  # my_int=123 my_str=None

print("\n--- Default value ---")
class MyModel(BaseModel):
    my_int: int = 123
    my_str: str

print(MyModel(my_str='foo'))  # my_int=123 my_str='foo'

print("\n--- Field default value ---")
## Field - used to customize and add metadata to fields of models
class MyModel(BaseModel):
    my_int: int = Field(123)
    my_str: str

print(MyModel(my_str='foo'))  # my_int=123 my_str='foo'

class MyModel(BaseModel):
    my_int: int 
    my_str: str = Field(default_factory=lambda: uuid4().hex)

print(MyModel(my_int=123))  # my_int=123 my_str='152fe8e55b6c4e8380f10e8be364bc96'

class MyModel(BaseModel):
    my_int: int = Field(default="twelve", validate_default=True)
    my_str: str

try:
    MyModel(my_str='foo')
except ValidationError as e:
    pprint.pp(e.errors()) # 'msg': 'Input should be a valid integer

print("\n--- Alias ---")
### Alias = an alternative name for a field, used when serializing and deserializing data

class MyModel(BaseModel):
    my_int: int 
    my_str: str = Field(alias='myString')

external_data = {'my_int': 123, 'myString': 'bar'}
print(MyModel(**external_data))  # my_int=123 my_str='bar'

external_data = {'my_int': 123, 'my_str': 'bar'}
try:
    MyModel(**external_data)
except ValidationError as e:
    pprint.pp(e.errors())  # 'msg': 'Field required'

print("\n--- Field frozen---")  
### Frozen = used to prevent the field from being assigned a new value after the model is created (immutability)
class MyModel(BaseModel):
    my_int: int = Field(frozen=True)
    my_str: str

my_model = MyModel(my_int=123, my_str='foo')
try:
    my_model.my_int = 456
except ValidationError as e:
    pprint.pp(e.errors())  # 'msg': 'Field is frozen',


class MyModel(BaseModel):
    my_dict: dict = Field(frozen=True)
    my_str: str

external_data = {'my_dict': {'a': 1}, 'my_str': 'foo'}
my_model = MyModel(**external_data)
my_model.my_dict['a'] = 2
print(my_model)  # my_dict={'a': 2} my_str='foo'
