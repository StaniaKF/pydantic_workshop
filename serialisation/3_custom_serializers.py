from datetime import datetime, timedelta
from typing import Annotated
from pydantic import BaseModel, PlainSerializer, SerializerFunctionWrapHandler, WrapSerializer, field_serializer, model_serializer