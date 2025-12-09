from pydantic import BaseModel
from typing import AnyStr


class Post(BaseModel):
    title: str
    content: str
