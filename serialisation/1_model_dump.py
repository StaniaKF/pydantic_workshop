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