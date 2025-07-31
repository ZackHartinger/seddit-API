from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from .core.database import create_db_and_tables, engine, SessionDep
from .models.db_models import Person
from .routers import person_router

@asynccontextmanager
async def lifespan(App: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(person_router.router)

@app.get("/")
def root():
    return {"message": "Hello World!"}

