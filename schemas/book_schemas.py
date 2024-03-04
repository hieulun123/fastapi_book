from typing import Union
from datetime import date
from pydantic import BaseModel


class BaseBook(BaseModel):
    title: str
    author: str
    publish_date: Union[date, None]
    isbn: str
    price: float


class BookCreate(BaseBook):
    pass


class BookUpdate(BaseBook):
    pass


class BookDetail(BaseBook):
    id: int

    class ConfigDict:
        from_attributes = True
