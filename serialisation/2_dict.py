from datetime import date
from pydantic import BaseModel, RootModel

# DOCUMENTATION: https://docs.pydantic.dev/latest/concepts/serialization/#dictmodel-and-iteration

class ChildModel(BaseModel):
    my_str: str

class ParentModel(BaseModel):
    my_str: str
    my_date: date
    my_child: ChildModel

parent = ParentModel(my_str='parent', my_date=date(2024, 11, 11), my_child=ChildModel(my_str='child'))
print(dict(parent))  
print(parent.model_dump())  

# {'my_str': 'parent', 'my_date': datetime.date(2024, 11, 11), 'my_child': ChildModel(my_str='child')}
# {'my_str': 'parent', 'my_date': datetime.date(2024, 11, 11), 'my_child': {'my_str': 'child'}}

class MyRootModel(RootModel):
    root: list[int]

my_root_model = MyRootModel([1,2,3])
print(dict(my_root_model))  
print(my_root_model.model_dump()) 
print(my_root_model.model_dump_json())   

# {'root': [1, 2, 3]}
# [1, 2, 3]
# [1,2,3]

print(type(dict(my_root_model)))
print(type(my_root_model.model_dump())) 
print(type(my_root_model.model_dump_json()))   

# <class 'dict'>
# <class 'list'>
# <class 'str'>