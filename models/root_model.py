import pprint
from pydantic import RootModel, ValidationError

##
# DOCUMENTATION: https://docs.pydantic.dev/latest/api/root_model/
# Pydantic models can be defined with a "custom root type"
# The root type can be any type supported by Pydantic
# For example, a root type can be a list or a dictionary

MyModel = RootModel[list[int]]
my_model = MyModel([1,2,3])
print(my_model) # root=[1, 2, 3]
print(my_model.model_dump()) # [1, 2, 3]

MyModel = RootModel[dict[str, int]]
my_model = MyModel({'a': 1, 'b': 2, 'c': 3})
print(my_model)  # root={'a': 1, 'b': 2, 'c': 3}
print(my_model.model_dump())  # {'a': 1, 'b': 2, 'c': 3}

try:
    my_model = MyModel({'a': 1, 'b': 'hello', 'c': 3})
except ValidationError as e:
    pprint.pp(e.errors()) # Input should be a valid integer, unable to parse string as an integer'

# to iterate over the data, you need to access the root attribute
for item in my_model.root:
    print(item)


print("--- Root Model bypassing the root attribute ---")
# to bypass the root attribute, define a custom model with dunder iter and getitem methods
class MyModel(RootModel):
    root: list[int]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]


my_model = MyModel([1,2,3])

for item in my_model:
    print(item)

print(my_model[0])



