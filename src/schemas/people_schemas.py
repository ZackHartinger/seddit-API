from typing import List
from .pet_schema import PetRead
from src.models.db_models import Person
from pydantic import BaseModel

class PersonRead(BaseModel) :
    id: int
    name: str
    age: int
    pets: list[PetRead] = []