### configuration - affects the behaviour of the entire model

import pprint
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from pydantic.alias_generators import to_camel


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

print("\n--- alias_generator---")
# alias_generator accepts a callable or AliasGenerator class

class MyModel(BaseModel):
    model_config = ConfigDict(alias_generator=lambda field_name: field_name.upper())

    my_int: int
    my_str: str

external_data = {"MY_INT": 123, "MY_STR": "abc"}

print(MyModel(**external_data))  # my_int=123 my_str='abc'

class MyModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    my_int: int
    my_str: str

external_data = {"myInt": 123, "myStr": "abc"}

print(MyModel(**external_data)) # my_int=123 my_str='abc'

print("\n--- arbitrary_types_allowed ---")
# allows you to combine normal classes with pydantic models
# # PydanticSchemaGenerationError is raised by default

class MyClass:
    def __init__(self, name: str):
        self.name = name

class MyModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    my_class: MyClass
    my_str: str

my_class = MyClass(name="abc")
my_model = MyModel(my_str="abc", my_class=my_class)
print(my_model)  # my_class=<__main__.MyClass object at 0x102aa1190> my_str='abc'

try:
    MyModel(my_str="abc", my_class="abc")
except ValidationError as e:
    print(e.errors())  # Input should be an instance of MyClass

my_class_2 = MyClass(name=4.2)
my_model_2 = MyModel(my_str="def", my_class=my_class)
print(my_model_2)  # my_class=<__main__.MyClass object at 0x100328980> my_str='def'

print("--- extra ---")
# to configure how pydantic handles the attributes that are not defined in the model
# pydantic models ignore extra fields by default

class MyModel(BaseModel):
    my_int: int
    my_str: str

external_data = {"my_int": 123, "my_str": "abc", "another_str": "edf"}

print(MyModel(**external_data))  # my_int=123 my_str='abc'

class MyModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    my_int: int
    my_str: str

external_data = {"my_int": 123, "my_str": "abc", "another_str": "edf"}

print(MyModel(**external_data))  # my_int=123 my_str='abc'

# forbit used not to allow any extra attributes 
class MyModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    my_int: int
    my_str: str

external_data = {"my_int": 123, "my_str": "abc", "another_str": "edf"}

try:
    MyModel(**external_data)
except ValidationError as e:
    pprint.pp(e.errors())  # Extra inputs are not permitted


# allow used to allow extra parameters
class MyModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    my_int: int
    my_str: str

external_data = {"my_int": 123, "my_str": "abc", "another_str": "edf"}

print(MyModel(**external_data))  # my_int=123 my_str='abc' another_str='edf'

print("\n--- frozen ---")

class MyModel(BaseModel):
    model_config = ConfigDict(frozen=True)

    my_dict: dict
    my_str: str

external_data = {"my_dict": {"a": 1, "b": 2}, "my_str": "abc"}
my_model = MyModel(**external_data)

try: 
    my_model.my_str = "ght"
except ValidationError as e:
    pprint.pp(e.errors())  # Instance is frozen

my_model.my_dict["a"] = 3

print("\n--- populate_by_name ---")
# Whether an aliased field may be populated by its name as given by the model attribute, as well as the alias

class MyModel(BaseModel):
    my_int: int
    my_str: str = Field(alias="my_string")

external_data = {"my_int": 123, "my_str": "abc"}

try: 
    my_model = MyModel(**external_data)
except ValidationError as e:
    pprint.pp(e.errors())  # Field required


class MyModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    my_int: int
    my_str: str = Field(alias="my_string")

external_data = {"my_int": 123, "my_str": "abc"}

print(MyModel(**external_data))  # my_int=123 my_str='abc'

external_data = {"my_int": 123, "my_string": "abc"}
print(MyModel(**external_data))  # my_int=123 my_str='abc'

print("--- validate_assignment ---")
# Whether to validate the data when the model is changed

class MyModel(BaseModel):
    my_int: int
    my_str: str

external_data = {"my_int": 123, "my_str": "abc"}
my_model = MyModel(**external_data)

my_model.my_int = "abc"

class MyModel(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    my_int: int
    my_str: str

external_data = {"my_int": 123, "my_str": "abc"}
my_model = MyModel(**external_data)

try:
    my_model.my_int = "abc"
except ValidationError as e:
    pprint.pp(e.errors()) # Input should be a valid integer, unable to parse string as an integer



