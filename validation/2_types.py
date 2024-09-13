from dataclasses import dataclass
from datetime import datetime
import pprint
from pydantic import BaseModel, Field, InstanceOf, PastDate, PastDatetime, SkipValidation, ValidationError, conlist

class MyModel(BaseModel):
    my_date: PastDatetime

print(MyModel(my_date=datetime.now()))

try:
    MyModel(my_date=datetime(2025,6,28))
except ValidationError as e:
    pprint.pp(e.errors()) # Date should be in the past

print("\n--- conlist ---")
class MyModel(BaseModel):
    my_list: conlist(str | int, min_length=1)

print(MyModel(my_list=["a", "b", 3]))

try:
    print(MyModel(my_list=[]))
except ValidationError as e:
    pprint.pp(e.errors()) 


class MyModel(BaseModel):
    my_list: list[str | int] = Field(min_length=1) 

print(MyModel(my_list=["a", "b", 3]))

try:
    print(MyModel(my_list=[]))
except ValidationError as e:
    pprint.pp(e.errors()) 

print("\n--- InstanceOf ---")
# InstanceOf is a type that can be used to validate that a value is an instance of a given class.

@dataclass
class Dog:
    name: str
    owner: str

@dataclass
class Poodle(Dog):
    ...

@dataclass
class Beagle(Dog):
    ...

class DogCompetition(BaseModel):
    dogs: list[Dog]

@dataclass
class Cat:
    name: str
    owner: str

dogs=[Poodle("Lucy", "Karl"), Beagle("Gifty", "John"), Cat("Missy", "Betty")]

try:    
    print(DogCompetition(dogs=dogs))    
except ValidationError as e:
    pprint.pp(e.errors())  # Input should be a dictionary or an instance of Dog


class DogCompetition(BaseModel):
    dogs: list[InstanceOf[Dog]]


try:    
    print(DogCompetition(dogs=dogs))
except ValidationError as e:
    pprint.pp(e.errors())  # Input should be a dictionary or an instance of Dog

print("\n--- SkipValidation ---")
# SkipValidation can be used to skip validation on a field

class DogCompetition(BaseModel):
    dogs: list[SkipValidation[Dog]]

print(DogCompetition(dogs=dogs))