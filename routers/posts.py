# app/routers/posts.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from models.post import Post
from schemas.post import PostCreate, PostOut

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts


@router.post("/", response_model=PostOut, status_code=201)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    # TEMP: hardcoded user (will be replaced by auth)
    fake_user_id = 1

    new_post = Post(
        title=post.title,
        content=post.content,
        owner_id=fake_user_id,
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
