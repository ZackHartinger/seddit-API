from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,Query
from sqlmodel import select, join
from src.models.db_models import User
from src.core.database import SessionDep
from src.schemas.user_schemas import UserRead, UserCreate
from sqlalchemy.orm import joinedload


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not Found"}},
)

@router.get("/", response_model=list[UserRead])
def read_users(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
) :
    people = session.exec(select(User).offset(offset).limit(limit).order_by(User.id)).all()
    return people

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, session: SessionDep) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/user/", response_model=UserRead)
def create_person(user: UserCreate, session: SessionDep) -> User:
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user