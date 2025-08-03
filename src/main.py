from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from .core.database import create_db_and_tables, engine, SessionDep
from .models.db_models import User, Post, Comment, Vote
from .routers import user_router

def seed_db_tables():
    with Session(engine) as session:
        zack = User(
            user_name="ztown", 
            email="zackhrtngr@gmail.com"
            )
        session.add(zack)
        session.commit()

        zacks_post = Post(
            user_id=zack.id,
            title="Zack's Post", 
            description="Zack's placeholder content. Zack's placeholder content. Zack's placeholder content. Zack's placeholder content. Zack's placeholder content. Zack's placeholder content."
            )
        session.add(zacks_post)
        session.commit()

        zacks_comment = Comment(
            user_id=zack.id,
            post_id=zacks_post.id,
            text="zacks comment"
        )
        session.add(zacks_comment)
        session.commit()

        zacks_reply = Comment(
            user_id=zack.id,
            post_id=zacks_post.id,
            reply_id=zacks_comment.id,
            text="zacks reply"
        )
        session.add(zacks_reply)
        session.commit()

        zacks_post_vote = Vote(
            user_id=zack.id,
            post_id=zacks_post.id
        )
        zacks_comment_vote = Vote(
            user_id=zack.id,
            comment_id=zacks_comment.id
        )
        session.add(zacks_post_vote, zacks_comment_vote)
        session.commit()

@asynccontextmanager
async def lifespan(App: FastAPI):
    create_db_and_tables()
    # seed_db_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(user_router.router)

@app.get("/")
def root():
    return {"message": "Hello World!"}

