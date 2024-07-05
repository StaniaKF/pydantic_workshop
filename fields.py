
from re import T
from pydantic.dataclasses import dataclass
from decimal import Decimal
import pprint
from typing import Optional
from pydantic import BaseModel, Field, ValidationError
from uuid import uuid4
from typing_extensions import Annotated

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

print("\n--- Annotated ---")
# Annotated = a special typing form to add context-specific metadata to an annotation

class MyModel(BaseModel):
    my_int: int
    my_str: Annotated[str, Field(default_factory=lambda: uuid4().hex)]

print(MyModel(my_int=123))

print("\n--- Numeric constraints ---")
# https://docs.pydantic.dev/latest/concepts/fields/#numeric-constraints

class MyModel(BaseModel):
    my_int: int = Field(default=123, gt=0)
    my_str: str

print(MyModel(my_int=45, my_str="abc"))  # my_int=45 my_str='abc'

try:
   MyModel(my_int=-45, my_str="abc") # Input should be greater than 0
except ValidationError as e:
    pprint.pp(e.errors())

print("\n--- String constraints ---")
### 3 string constraints: min_length, max_length, pattern

class MyModel(BaseModel):
    my_int: int 
    my_str: str = Field(min_length=3) 

try:
   MyModel(my_int=45, my_str="ab") 
except ValidationError as e:
    pprint.pp(e.errors()) # String should have at least 3 characters

class MyModel(BaseModel):
    my_int: int 
    my_str: str = Field(pattern=r'^\d*$') ### ^\d = start with a number, * = occuring 0 or more times, $ = match everything from start to end

try:
   MyModel(my_int=45, my_str="123b") 
except ValidationError as e:
    pprint.pp(e.errors())  # String should match pattern '^\\d*$


print("\n--- Decimal constraints ---")
### Two decimal constraints: max_digits, decimal_places

class MyModel(BaseModel):
    my_int: int 
    my_decimal: Decimal = Field(decimal_places=2) 

try:
   MyModel(my_int=45, my_decimal=Decimal("23.455")) 
except ValidationError as e:
    pprint.pp(e.errors()) # Decimal input should have no more than 2 decimal places


print("\n--- Dataclass constraints ---")
### init: Whether the field should be included in the __init__ of the dataclass.

@dataclass
class MyDataClass:
    my_int: int = Field(init=True)

class MyModel(BaseModel):
    my_dataclass: MyDataClass

try: 
    my_dataclass = MyDataClass()
except ValidationError as e:
    pprint.pp(e.errors())

### init_var: Whether the field should be seen as an init-only field in the dataclass
@dataclass
class MyDataClass:
    my_int: int = Field(init=True)
    my_init_var: str= Field(init_var=True)

class MyModel(BaseModel):
    my_dataclass: MyDataClass

my_dataclass = MyDataClass(my_int=123, my_init_var='foo')
my_model = MyModel(my_dataclass=my_dataclass)

print(my_model.model_dump())  # {'my_dataclass': {'my_int': 123}}

# kw_only: Whether the field should be a keyword-only argument in the constructor of the dataclass
@dataclass
class MyDataClass:
    my_kw_only: str = Field(kw_only=True)

try:
    print(MyDataClass("hello"))
except ValidationError as e:
    pprint.pp(e.errors())  # unexpected_positional_argument'

### https://docs.pydantic.dev/latest/concepts/fields/




