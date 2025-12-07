from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from routers import posts
from passlib.context import CryptContext
from database import Base, engine, SessionLocal
import models
import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


app = FastAPI()
app.include_router(posts.router)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# @app.get("/posts")
# async def get_posts():
#     return {"data": "This is your posts"}
