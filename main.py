from fastapi import FastAPI, Depends, HTTPException
from routers import posts

app = FastAPI()
app.include_router(posts.router)

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# @app.get("/posts")
# async def get_posts():
#     return {"data": "This is your posts"}
