from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,Query
from sqlmodel import select, join, func
from src.models.db_models import Vote
from src.core.database import SessionDep
from src.schemas.vote_schema import VoteRead, PostVoteRead, CommentVoteRead, PostVoteCreate, CommentVoteCreate

router = APIRouter(
    prefix="/votes",
    tags=["votes"],
    responses={404: {"description": "Not Found"}},
)

@router.get("/", response_model=list[VoteRead])
def read_votes(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
) :
    people = session.exec(select(Vote).offset(offset).limit(limit).order_by(Vote.id)).all()
    return people

@router.get("/post_vote_total/{post_id}")
def read_post_vote_total(
    session: SessionDep,
    post_id: int,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) :
    post_vote_total = session.exec(select(func.sum(Vote.vote_value)).where(Vote.post_id == post_id)).one()
    return post_vote_total

@router.get("/comment_vote_total/{comment_id}")
def read_comment_vote_total(
    session: SessionDep,
    comment_id: int,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) :
    comment_vote_total = session.exec(select(func.sum(Vote.vote_value)).where(Vote.comment_id == comment_id)).one()
    return comment_vote_total

@router.post("/post_vote", response_model=PostVoteRead)
def create_post_vote(vote: PostVoteCreate, session: SessionDep) -> Vote:
    check_vote = session.exec(select(Vote).where(Vote.user_id == vote.user_id, Vote.post_id == vote.post_id)).first()
    if check_vote :
        raise HTTPException(400, "Cannot vote again.")
    else:
        db_vote = Vote.model_validate(vote)
        session.add(db_vote)
        session.commit()
        session.refresh(db_vote)
        return db_vote

@router.post("/comment_vote", response_model=CommentVoteRead)
def create_comment_vote(vote: CommentVoteCreate, session: SessionDep) -> Vote:
    check_vote = session.exec(select(Vote).where(Vote.user_id == vote.user_id, Vote.comment_id == vote.comment_id)).first()
    if check_vote :
        raise HTTPException(400, "Cannot vote again.")
    else:
        db_vote = Vote.model_validate(vote)
        session.add(db_vote)
        session.commit()
        session.refresh(db_vote)
        return db_vote

@router.patch("/up_vote/{vote_id}")
def up_vote(vote_id: int, session: SessionDep):
    vote_db = session.get(Vote, vote_id)
    if not vote_db:
        raise HTTPException(404, "Vote not found")
    vote_db.vote_value = 1
    session.add(vote_db)
    session.commit()
    session.refresh(vote_db)
    return vote_db

@router.patch("/down_vote/{vote_id}")
def down_vote(vote_id: int, session: SessionDep):
    vote_db = session.get(Vote, vote_id)
    if not vote_db:
        raise HTTPException(404, "Vote not found")
    vote_db.vote_value = 0
    session.add(vote_db)
    session.commit()
    session.refresh(vote_db)
    return vote_db