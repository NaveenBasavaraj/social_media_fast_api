# app/schemas/post.py
from datetime import datetime
from pydantic import BaseModel


# -----------------
# Base (shared)
# -----------------
class PostBase(BaseModel):
    title: str
    content: str


# -----------------
# Create (request)
# -----------------
class PostCreate(PostBase):
    pass


# -----------------
# Update (request)
# -----------------
class PostUpdate(PostBase):
    published: bool | None = None


# -----------------
# Response
# -----------------
class PostOut(PostBase):
    id: int
    owner_id: int
    published: bool
    created_at: datetime

    class Config:
        orm_mode = True
