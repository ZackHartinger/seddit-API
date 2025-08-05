from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,Query
from sqlmodel import select, join
from src.models.db_models import Vote
from src.core.database import SessionDep
from src.schemas.vote_schema import VoteRead, VoteCreate

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

@router.post("/vote", response_model=VoteRead)
def create_vote(vote: VoteCreate, session: SessionDep) -> Vote:
    db_vote = Vote.model_validate(vote)
    session.add(db_vote)
    session.commit()
    session.refresh(db_vote)
    return db_vote