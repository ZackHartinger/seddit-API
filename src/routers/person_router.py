from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,Query
from sqlmodel import select
from src.core.database import SessionDep
from src.models.db_models import Person

router = APIRouter(
    prefix="/people",
    tags=["people"],
    responses={404: {"description": "Not Found"}},
)

@router.get("/")
def read_people(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
) :
    people = session.exec(select(Person).offset(offset).limit(limit).order_by(Person.id)).all()
    return people

@router.post("/person/")
def create_person(person: Person, session: SessionDep) -> Person:
    session.add(person)
    session.commit()
    session.refresh(person)
    return person