from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar('T')


class ResponseBase(BaseModel, Generic[T]):
    status: str
    message: str
    data: T | None = None
