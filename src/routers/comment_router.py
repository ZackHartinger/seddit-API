from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,Query
from sqlmodel import select, join
from src.models.db_models import Comment
from src.core.database import SessionDep
from src.schemas.comment_schema import CommentRead, CommentCreate

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
    responses={404: {"description": "Not Found"}},
)

@router.get("/", response_model=list[CommentRead])
def read_comments(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
) :
    people = session.exec(select(Comment).offset(offset).limit(limit).order_by(Comment.id)).all()
    return people

@router.post("/comment", response_model=CommentRead)
def create_comment(comment: CommentCreate, session: SessionDep) -> Comment:
    db_comment = Comment.model_validate(comment)
    session.add(db_comment)
    session.commit()
    session.refresh(db_comment)
    return db_comment