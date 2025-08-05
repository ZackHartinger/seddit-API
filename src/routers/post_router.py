from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,Query
from sqlmodel import select, join
from src.models.db_models import Post
from src.core.database import SessionDep
from src.schemas.post_schemas import PostCreate, PostRead

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not Found"}},
)

@router.get("/", response_model=list[PostRead])
def read_posts(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
) :
    people = session.exec(select(Post).offset(offset).limit(limit).order_by(Post.id)).all()
    return people

@router.post("/post", response_model=PostRead)
def create_post(post: PostCreate, session: SessionDep) -> Post:
    db_post = Post.model_validate(post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post