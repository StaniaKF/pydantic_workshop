from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field, Json, ValidationError

# Pydantic uses the terms "serialize" and "dump" interchangeably. 
# Both refer to the process of converting a model to a dictionary or JSON-encoded string.
# To convert your model to a dictionary, you can use the model_dump method
# DOCUMENTATION: https://docs.pydantic.dev/2.9/api/base_model/#pydantic.BaseModel.model_dump

print("--- model.model_dump ---")
# Converts your model to a dictionary

class MyModel(BaseModel):
    my_int: int
    my_str: str

my_model = MyModel(my_int=123, my_str='abc')
serialised_model = my_model.model_dump()
print(serialised_model) # {'my_int': 123, 'my_str': 'abc'}

# model_dump has several parameters that allow you to customise the output

# mode: str | Literal['json', 'python'] = 'python',
# include: IncEx = None,
# exclude: IncEx = None,
# exclude_unset: bool = False,
# exclude_defaults: bool = False,
# exclude_none: bool = False,
# by_alias: bool = False,
# round_trip: bool = False,
# warnings: bool | Literal['none', 'warn', 'error'] = True,
# serialize_as_any: bool = False
# context: dict[str, Any] | None = None,

print("\n--- model.model_dump mode ---")
# determines if the output should contain only JSON serializable types or if it should contain non-JSON-serializable types

class MyModel(BaseModel):
    my_dec: Decimal
    my_date: date

my_model = MyModel(my_dec=Decimal('123.456'), my_date=date(2021, 1, 1))
serialised_model = my_model.model_dump(mode='python')
print(serialised_model) # {'my_dec': Decimal('123.456'), 'my_date': datetime.date(2021, 1, 1)}
serialised_model = my_model.model_dump(mode='json')
print(serialised_model)  # {'my_dec': '123.456', 'my_date': '2021-01-01'}
serialised_model = my_model.model_dump()
print(serialised_model) # {'my_dec': Decimal('123.456'), 'my_date': datetime.date(2021, 1, 1)}

print("\n--- model.model_dump include ---")
# determines the set of fields to include in the output

class MyModel(BaseModel):
    my_int: int
    my_str: str

my_model = MyModel(my_int=123, my_str='abc')
serialised_model = my_model.model_dump(include={'my_int'})
print(serialised_model) # {'my_int': 123}

# we can also pass in a dictionary, allowing nested selection of which fields to export
class MyNestedModel(BaseModel):
    my_int: int
    my_str: str

class MyModel(BaseModel):
    my_int: int
    my_str: str
    my_nested_model: MyNestedModel

my_model = MyModel(my_int=123, my_str='abc', my_nested_model=MyNestedModel(my_int=456, my_str='def'))

keys_to_include = {
    "my_int": True,
    "my_nested_model": {"my_str"}
}

serialised_model = my_model.model_dump(include=keys_to_include)
print(serialised_model)  # {'my_int': 123, 'my_nested_model': {'my_str': 'def'}}

class MyModel(BaseModel):
    my_list: list[MyNestedModel]

my_model = MyModel(
    my_list=[
        MyNestedModel(my_int=1, my_str='a'), 
        MyNestedModel(my_int=2, my_str='b'), 
        MyNestedModel(my_int=3, my_str='c')
        ]
    )

keys_to_include = {
    "my_list": {0: True, -1: {"my_int"}}
}

serialised_model = my_model.model_dump(include=keys_to_include)
print(serialised_model) # {'my_list': [{'my_int': 1, 'my_str': 'a'}, {'my_int': 3}]}


print("\n--- model.model_dump exclude ---")
# determines the set of fields to exclude in the output

class MyModel(BaseModel):
    my_int: int
    my_str: str

my_model = MyModel(my_int=123, my_str='abc')
serialised_model = my_model.model_dump(exclude={'my_int'})
print(serialised_model) # {'my_str': 'abc'}

class MyNestedModel(BaseModel):
    my_int: int
    my_str: str # <- excluded

class MyModel(BaseModel):
    my_int: int # <- excluded
    my_str: str
    my_nested_model: MyNestedModel

my_model = MyModel(my_int=123, my_str='abc', my_nested_model=MyNestedModel(my_int=456, my_str='def'))

keys_to_exclude = {
    "my_int": True,
    "my_nested_model": {"my_str"}
}

serialised_model = my_model.model_dump(exclude=keys_to_exclude)
print(serialised_model) # {'my_str': 'abc', 'my_nested_model': {'my_int': 456}}

# it is also possible to exclude fields at the field level

class MyModel(BaseModel):
    my_int: int = Field(exclude=True)
    my_str: str

my_model = MyModel(my_int=123, my_str='abc')
serialised_model = my_model.model_dump()
print(serialised_model) # {'my_str': 'abc'}

# Setting exclude on the field constructor (Field(exclude=True)) takes priority over the include on model_dump and model_dump_json

serialised_model = my_model.model_dump(include={"my_int"})
print(serialised_model) # {}

class MyModel(BaseModel):
    my_int: int = Field(exclude=False)
    my_str: str

my_model = MyModel(my_int=123, my_str='abc')
serialised_model = my_model.model_dump(exclude={"my_int"})
print(serialised_model)  # {'my_str': 'abc'}


print("\n--- model.model_dump exclude_unset ---")
# Determines whether to exclude fields that have not been explicitly set.

class MyModel(BaseModel):
    my_int: int 
    my_str: str | None = None

external_data = {"my_int": 123}
my_model = MyModel(**external_data)

serialised_model = my_model.model_dump()
print(serialised_model) # {'my_int': 123, 'my_str': None}

serialised_model = my_model.model_dump(exclude_unset=True)
print(serialised_model) # {'my_int': 123}

external_data = {"my_int": 123, "my_str": None}
my_model = MyModel(**external_data)
serialised_model = my_model.model_dump(exclude_unset=True)
print(serialised_model) # {'my_int': 123, 'my_str': None}

# exclude_unset, exclude_defaults, exclude_none on model_dump take a priority over negative exclusion at the field level
# DOCUMENTATION: https://docs.pydantic.dev/latest/concepts/serialization/#model-and-field-level-include-and-exclude

class MyModel(BaseModel):
    my_int: int 
    my_str: str | None = Field(None, exclude=False)

external_data = {"my_int": 123}
my_model = MyModel(**external_data)
serialised_model = my_model.model_dump()
print(serialised_model) # {'my_int': 123, 'my_str': None}

serialised_model = my_model.model_dump(exclude_unset=True)
print(serialised_model) # {'my_int': 123}

print("\n--- model.model_dump exclude_none ---")
# To exclude fields that are None

class MyModel(BaseModel):
    my_int: int 
    my_str: str | None = None

external_data = {"my_int": 123, "my_str": None}
my_model = MyModel(**external_data)

serialised_model = my_model.model_dump(exclude_none=True)
print(serialised_model) # {"my_int": 123}

print("\n--- model.model_dump exclude_defaults ---")
# To exclude fields that have default values

class MyModel(BaseModel):
    my_int: int
    my_str: str  = "abc"

external_data = {"my_int": 123}
my_model = MyModel(**external_data)

serialised_model = my_model.model_dump()
print(serialised_model) # {'my_int': 123, 'my_str': 'abc'}

serialised_model = my_model.model_dump(exclude_defaults=True)
print(serialised_model) # {'my_int': 123}

print("\n--- model.model_dump by_alias ---")
# Determines if to use the field's alias in the dictionary key of the serialised output 

class MyModel(BaseModel):
    my_int: int 
    my_str: str = Field(alias="myString")

external_data = {"my_int": "123", "myString": "abc"}
my_model = MyModel(**external_data)

print(my_model) # my_int=123 my_str='abc'

serialised_model = my_model.model_dump()
print(serialised_model) # {'my_int': 123, 'my_str': 'abc'}

serialised_model = my_model.model_dump(by_alias=True)
print(serialised_model) # {'my_int': 123, 'myString': 'abc'}

class MyModel(BaseModel):
    my_int: int 
    my_str: str = Field(serialization_alias="myString")

external_data = {"my_int": "123", "my_str": "abc"}
my_model = MyModel(**external_data)
serialised_model = my_model.model_dump(by_alias=True)
print(serialised_model) # {'my_int': 123, 'myString': 'abc'}

external_data = {"my_int": "123", "myString": "abc"}
try: 
    MyModel(**external_data)
except ValidationError as e:
    print(e.errors())

print("\n--- model.model_dump round_trip ---")
# If True, dumped values should be valid as input for non-idempotent types such as Json[T].

class MyModel(BaseModel):
    my_json: Json[list[int]]

external_data = {"my_json": "[1, 2, 3]"}
my_model = MyModel(**external_data)
print(my_model.model_dump()) # {'my_json': [1, 2, 3]}
print(my_model.model_dump(round_trip=True)) # {'my_json': '[1,2,3]'}

print("\n--- model.model_dump warning ---")
# determines how warnings should be handled
# will be covered after PlainSerializer

print("\n--- model.model_dump serialize_as_any ---")
# will be covered when we talk about serialising subclasses and serialising with duck-typing

print("\n--- model.model_dump context ---")
# will be covered after field_serializer decorator

print("\n--- model.model_dump_json ---")
# model_dump_json serializes a model directly to a JSON-encoded string that is 
# equivalent to the result produced by .model_dump()
# it takes the same parameters as model_dump except it takes an indent parameter
# instead of the mode parameter

class MyModel(BaseModel):
    my_int: int 
    my_str: str 

external_data = {"my_int": "123", "my_str": "abc"}
my_model = MyModel(**external_data)

print(type(my_model.model_dump())) 
print(my_model.model_dump()) 

print(type(my_model.model_dump_json())) 
print(my_model.model_dump_json()) 

print(my_model.model_dump_json(indent=2)) 

# <class 'dict'>
# {'my_int': 123, 'my_str': 'abc'}

# <class 'str'>
# {"my_int":123,"my_str":"abc"}

# {
#   "my_int": 123,
#   "my_str": "abc"
# }