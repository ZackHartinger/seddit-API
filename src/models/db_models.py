from typing import  Optional
from sqlmodel import SQLModel, Field, Session, Relationship
from src.core.database import engine

class Person(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field
    age: int | None = Field(default=None, index=True)
    secret_name: str

    pets: list["Pet"] = Relationship(back_populates="person", sa_relationship_kwargs={"lazy": "selectin"})

class Pet(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field
    type: str = Field

    person_id: int | None = Field(default=None, foreign_key="person.id")
    person: Person | None = Relationship(back_populates="pets")

# def create_owners_and_pets():
#     with Session(engine) as session:
#         zack = Person(name="Zack", age=31, secret_name="ZTOWN")
#         session.add(zack)
#         session.commit()

#         theo = Pet(name="Theo", type="Cat", person_id=zack.id)
#         session.add(theo)
#         session.commit()

#         print(zack.pets)