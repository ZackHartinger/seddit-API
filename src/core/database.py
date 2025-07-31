from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine

server_name = "(localdb)\\mssqllocaldb"
db_name = "fastapitest"

sql_url = f"mssql+pyodbc://@{server_name}/{db_name}?trusted_connection=yes&driver=ODBC+Driver+18+for+SQL+Server"

connect_args = {"check_same_thread": False}
engine = create_engine(sql_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]