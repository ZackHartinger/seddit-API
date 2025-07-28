from typing import Annotated
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Person(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field
    age: int | None = Field(default=None, index=True)
    secret_name: str

server_name = "(localdb)\\mssqllocaldb"
db_name = "fastapitest"

sql_url = f"mssql+pyodbc://@{server_name}/{db_name}?trusted_connection=yes&driver=ODBC+Driver+18+for+SQL+Server"
# sql_url =  "mssql+pyodbc:///?odbc_connect=DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\\MSSQLLocalDB;DATABASE=fastapitest;Trusted_Connection=yes;"

connect_args = {"check_same_thread": False}
engine = create_engine(sql_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(App: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "Hello World!"}

@app.post("/person/")
def create_person(person: Person, session: SessionDep) -> Person:
    session.add(person)
    session.commit()
    session.refresh(person)
    return person

@app.get("/people/", response_model=list[Person])
def read_people(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
) :
    people = session.exec(select(Person).offset(offset).limit(limit).order_by(Person.id)).all()
    return people