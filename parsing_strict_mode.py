from decimal import Decimal
from pydantic import BaseModel

print("\n--- Data coercion: lax mode ---")
# https://docs.pydantic.dev/latest/concepts/conversion_table/

class MyModel(BaseModel):
    my_int: int
    my_str: str

external_data = {"my_int": "123", "my_str": "abc"}
my_model = MyModel(**external_data)

print(type(my_model.my_int))  # <class 'int'>

class MyModel(BaseModel):
    my_number: Decimal
    my_str: str

external_data = {"my_number": 12.35, "my_str": "abc"}
my_model = MyModel(**external_data)

print(type(my_model.my_number))  # <class 'decimal.Decimal'>