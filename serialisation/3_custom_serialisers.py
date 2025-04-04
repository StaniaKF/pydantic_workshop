from datetime import datetime, timedelta
from typing import Annotated
from pydantic import BaseModel, PlainSerializer, SerializerFunctionWrapHandler, WrapSerializer, field_serializer, model_serializer

# DOCUMENTATION: https://docs.pydantic.dev/latest/concepts/serialization/#custom-serializers
# Pydantic provides several functional serializers to customise how a model is serialized to a dictionary or JSON.

# @field_serializer
# @model_serializer
# PlainSerializer
# WrapSerializer

print("--- @field_serializer ---")
# Serialization can be customised on a field using the @field_serializer decorator
# A single serializer can also be called on all fields by passing the special value '*' to the @field_serializer decorator.

class MyModel(BaseModel):
    my_datetime: datetime

my_model = MyModel(my_datetime=datetime(2021, 1, 1, 12, 0, 0))
print(my_model.model_dump()) # {'my_datetime': datetime.datetime(2021, 1, 1, 12, 0)}
print(my_model.model_dump(mode="json")) # {'my_datetime': '2021-01-01T12:00:00'}

class MyModel(BaseModel):
    my_datetime: datetime

    @field_serializer("my_datetime")
    def serialise_my_datatime(self, value: datetime) -> float:
        return value.timestamp()

my_model = MyModel(my_datetime=datetime(2021, 1, 1, 12, 0, 0))
print(my_model.model_dump()) # {'my_datetime': 1609502400.0}


print("\n--- @model_serializer ---")
# Serialization can be customised on a model using the @model_serializer decorator

class MyModel(BaseModel):
    my_datetime: datetime

    @model_serializer
    def serialise_my_model(self) -> dict[str, float]:
        return {"my_datetime_as_epoch": self.my_datetime.timestamp()}

my_model = MyModel(my_datetime=datetime(2021, 1, 1, 12, 0, 0))
print(my_model.model_dump())  # {'my_datetime_as_epoch': 1609502400.0}

print("\n--- PlainSerializer ---")
# PlainSerializer and WrapSerializer enable you to use a function to modify the output of serialization
# Both serializers accept optional arguments including:
    # return_type: specifies the return type for the function. If omitted it will be inferred from the type annotation.
    # when_used: specifies when this serializer should be used. 
        # Accepts a string with values 'always', 'unless-none', 'json', and 'json-unless-none'. Defaults to 'always'.

type MyDatetime = Annotated[
    datetime, 
    PlainSerializer(lambda x: x.timestamp(), return_type=float, when_used='json')
]

class MyModel(BaseModel):
    my_datetime: MyDatetime

my_model = MyModel(my_datetime=datetime(2021, 1, 1, 12, 0, 0))
print(my_model.model_dump()) # {'my_datetime': datetime.datetime(2021, 1, 1, 12, 0)}
print(my_model.model_dump_json()) # {"my_datetime":1609502400.0}
print(my_model.model_dump(mode="json")) # {'my_datetime': 1609502400.0}

def to_timestamp(value: datetime) -> float:
    return value.timestamp()

type MyDatetime = Annotated[
    datetime, 
    PlainSerializer(to_timestamp, return_type=float, when_used='json')
]

class MyModel(BaseModel):
    my_datetime: MyDatetime

my_model = MyModel(my_datetime=datetime(2021, 1, 1, 12, 0, 0))

print(my_model.model_dump_json()) # {"my_datetime":1609502400.0}

print("\n--- WrapSerializer ---")
# in contrast to the plainSerializer,
# the wrap serializer receives the raw inputs along with a handler function that applies the standart serialization logic
# and can modify the resulting value before returning it as the final output of serialization

def transform_timestamp(value: datetime, handler: SerializerFunctionWrapHandler) -> datetime:
    final_value = value + timedelta(days=1)
    return handler(final_value)

type MyDatetime = Annotated[
    datetime, 
    WrapSerializer(transform_timestamp, return_type=str | datetime, when_used='always')
]

class MyModel(BaseModel):
    my_datetime: MyDatetime

my_model = MyModel(my_datetime=datetime(2021, 1, 1, 12, 0, 0))
print(my_model.model_dump()) # {'my_datetime': datetime.datetime(2021, 1, 2, 12, 0)}
print(my_model.model_dump_json()) # {"my_datetime":"2021-01-02T12:00:00"}


    












    


