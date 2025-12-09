from fastapi import FastAPI, Depends, HTTPException
from routers import posts

# Ensure models are imported so SQLAlchemy registers the tables
import models  # noqa: F401

from db.base import Base
from db.session import engine
import time
from sqlalchemy.exc import OperationalError

app = FastAPI()
app.include_router(posts.router)


@app.on_event("startup")
def on_startup():
    """Create database tables on application startup if they don't exist."""
    # Wait for the database to be available (useful when running in Docker)
    max_tries = 10
    for attempt in range(1, max_tries + 1):
        try:
            with engine.connect():
                break
        except OperationalError:
            if attempt == max_tries:
                raise
            time.sleep(2)

    Base.metadata.create_all(bind=engine)


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# @app.get("/posts")
# async def get_posts():
#     return {"data": "This is your posts"}
