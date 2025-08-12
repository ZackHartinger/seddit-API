from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,Query
from sqlmodel import select, join
from src.models.db_models import Post, Comment
from src.core.database import SessionDep
from src.schemas.post_schemas import PostCreate, PostRead, PostEdit
from src.routers.vote_router import read_post_vote_total, read_comment_vote_total

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
    posts = session.exec(select(Post).offset(offset).limit(limit).order_by(Post.id)).all()
    for post in posts:
        post.post_vote_total = read_post_vote_total(session, post.id)
        for comment in post.post_comments:
            comment.comment_vote_total = read_comment_vote_total(session, comment.id)

    return posts

@router.get("/{post_id}", response_model=PostRead)
def read_post(post_id: int, session: SessionDep) -> Post:
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")
    if post:
        post.post_vote_total = read_post_vote_total(session, post.id)
    return post

@router.post("/post", response_model=PostRead)
def create_post(post: PostCreate, session: SessionDep) -> Post:
    db_post = Post.model_validate(post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post

@router.patch("/{post_id}", response_model=PostRead)
def edit_post(post_id: int, post: PostEdit, session: SessionDep) -> Post:
    db_post = session.get(Post, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    db_post.title = post.title
    db_post.description = post.description
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post

@router.delete("/{post_id}", response_model=PostRead)
def delete_post(post_id:int, session: SessionDep) -> Post:
    db_post = session.get(Post, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    session.delete(db_post)
    session.commit()
    return db_post