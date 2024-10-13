from pydantic import AliasPath, AliasChoices, BaseModel, Field

# # DOCUMENTATION: https://docs.pydantic.dev/2.9/concepts/alias/
print("--- validation_alias ---")

class MyModel(BaseModel):
    my_int: int 
    my_str: str = Field(alias="myString")

external_data = {"my_int": "123", "myString": "abc"}
my_model = MyModel(**external_data)
print(my_model)  # my_int=123 my_str='abc'
print(my_model.model_dump(by_alias=True)) # {'my_int': 123, 'myString': 'abc'}

class MyModel(BaseModel):
    my_int: int 
    my_str: str = Field(validation_alias="myString")


my_model = MyModel(**external_data)
print(my_model) # my_int=123 my_str='abc'
print(my_model.model_dump(by_alias=True)) # {'my_int': 123, 'my_str': 'abc'}


print("\n--- AliasPath ---")
# The AliasPath is used to specify a path to a field using aliases

my_string_values = {"my_strings": ["abc", "def"]}

class MyModel(BaseModel):
    my_str_1: str = Field(validation_alias=AliasPath("my_strings", 0))
    my_str_2: str = Field(validation_alias=AliasPath("my_strings", 1))

my_model = MyModel(**my_string_values)
print(my_model) # my_str_1='abc' my_str_2='def'

print("\n--- AliasChoices ---")
# AliasChoices is used to specify a choice of aliases

class MyModel(BaseModel):
    my_str_1: str = Field(validation_alias=AliasChoices("myString1", "myStringA"))
    my_str_2: str

external_data = {"myString1": "abc", "my_str_2": "def"}
my_model = MyModel(**external_data)
print(my_model)

external_data = {"myStringA": "abc", "my_str_2": "def"}
my_model = MyModel(**external_data)
print(my_model) 

external_data = {"myStringA": "abcA", "my_str_2": "def", "myString1": "abcB"}
my_model = MyModel(**external_data)
print(my_model) # my_str_1='abcB' my_str_2='def'

print("\n--- AliasChoices + AliasPath ---")
class MyModel(BaseModel):
    my_str_1: str = Field(validation_alias=AliasChoices("myString1", AliasPath("my_strings", 0)))
    my_str_2: str = Field(validation_alias=AliasChoices("myString2",AliasPath("my_strings", 1)))

my_string_values = {"my_strings": ["abc", "def"]}

my_model = MyModel(**my_string_values)
print(my_model)  # my_str_1='abc' my_str_2='def'

my_model = MyModel(**my_string_values, **{"myString2": "ghi"})
print(my_model) # my_str_1='abc' my_str_2='ghi'