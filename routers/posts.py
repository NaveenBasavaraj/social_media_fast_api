from fastapi import APIRouter
from fastapi.params import Body

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/posts")
async def get_posts():
    return {"data": "This is your posts"}


@router.post("/createposts")
async def create_posts(payload: dict = Body(...)):
    print(f"{payload}")
    return {"payload": payload}
