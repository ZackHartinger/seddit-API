from typing import  Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Session, Relationship
from src.core.database import engine

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_name: str = Field
    email: str = Field

    posts: list["Post"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    user_comments: list["Comment"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    user_votes: list["Vote"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})

class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at : datetime = Field(default_factory=datetime.now)
    title: str = Field
    description: str | None = Field(default=None)

    user_id: int | None = Field(default=None, foreign_key="user.id")
    user: User | None = Relationship(back_populates="posts")

    post_comments: list["Comment"] = Relationship(back_populates="post",sa_relationship_kwargs={"lazy": "selectin"})
    post_votes: list["Vote"] = Relationship(back_populates="post",sa_relationship_kwargs={"lazy": "selectin"})

class Comment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str = Field

    reply_id: int | None = Field(default=None, foreign_key="comment.id")
    parent_comment: Optional["Comment"] = Relationship(back_populates="replies", sa_relationship_kwargs={"remote_side": "Comment.id"})
    replies: list["Comment"] = Relationship(back_populates="parent_comment", sa_relationship_kwargs={"lazy":"selectin"})

    post_id: int | None = Field(default=None, foreign_key="post.id")
    post: Post | None = Relationship(back_populates="post_comments")

    user_id: int | None = Field(default=None, foreign_key="user.id")
    user: User | None = Relationship(back_populates="user_comments")

    comment_votes: list["Vote"] = Relationship(back_populates="comment",sa_relationship_kwargs={"lazy": "selectin"})

class Vote(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    vote_value: int = Field

    post_id: int | None = Field(default=None, foreign_key="post.id")
    post: Post | None = Relationship(back_populates="post_votes")

    user_id: int | None = Field(default=None, foreign_key="user.id")
    user: User | None = Relationship(back_populates="user_votes")

    comment_id: int | None = Field(default=None, foreign_key="comment.id")
    comment: Comment | None = Relationship(back_populates="comment_votes")





# def create_owners_and_pets():
#     with Session(engine) as session:
#         zack = Person(name="Zack", age=31, secret_name="ZTOWN")
#         session.add(zack)
#         session.commit()

#         theo = Pet(name="Theo", type="Cat", person_id=zack.id)
#         session.add(theo)
#         session.commit()

#         print(zack.pets)