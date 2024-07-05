### configuration - affects the behaviour of the entire model

import pprint
from pydantic import BaseModel, ConfigDict, Field, ValidationError


class MyModel(BaseModel):
    my_int: int 
    my_str: str = Field(min_length=3) 


print("\n--- Basic config usage ---")

class MyModel(BaseModel):
    model_config = ConfigDict(str_min_length=3)

    my_str_1: str 
    my_str_2: str

external_data = {"my_str_1": "abc", "my_str_2": "a"}

try:
    MyModel(**external_data)
except ValidationError as e:
    pprint.pp(e.errors())  # String should have at least 3 characters


class MyModel(BaseModel, str_min_length=3):

    my_str_1: str 
    my_str_2: str

try:
    MyModel(**external_data)
except ValidationError as e:
    pprint.pp(e.errors())  # String should have at least 3 characters


class MyModel(BaseModel, str_min_length=3):

    my_str_1: str 
    my_str_2: str = Field(min_length=1)

print(MyModel(**external_data))  # my_str_1='abc' my_str_2='a'

# https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict

# our BaseModel in smarter tariff common library
# https://github.com/upside-energy/smarter-tariff/blob/24d4400829af44e735ee1327b25f2df01a56494c/libraries/smarter-tariff-common/smarter_tariff_common/models/base_models.py#L17



