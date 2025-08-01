from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,Query
from sqlmodel import select, join
from src.core.database import SessionDep
from src.models.db_models import Person, Pet
from sqlalchemy.orm import joinedload
from src.schemas.people_schemas import PersonRead

router = APIRouter(
    prefix="/people",
    tags=["people"],
    responses={404: {"description": "Not Found"}},
)

@router.get("/", response_model=list[PersonRead])
def read_people(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
) :
    people = session.exec(select(Person).offset(offset).limit(limit).order_by(Person.id)).all()
    # print(people)
    return people

@router.post("/person/")
def create_person(person: Person, session: SessionDep) -> Person:
    session.add(person)
    session.commit()
    session.refresh(person)
    return person
