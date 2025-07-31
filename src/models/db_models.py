from sqlmodel import SQLModel, Field

class Person(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field
    age: int | None = Field(default=None, index=True)
    secret_name: str