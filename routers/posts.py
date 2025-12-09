from fastapi import APIRouter
from fastapi.params import Body
from models import Post

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/posts")
async def get_posts():
    return {"data": "This is your posts"}


@router.post("/createposts")
async def create_posts(new_post: Post):  # (payload: dict = Body(...))
    print(f"{new_post}")
    return {"title": new_post.title}
