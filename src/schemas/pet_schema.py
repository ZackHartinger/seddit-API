from sqlmodel import SQLModel
from pydantic import BaseModel

class PetRead(BaseModel):
    id: int
    name: str
    type: str
