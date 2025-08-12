from pydantic import BaseModel
from .vote_schema import VoteRead
from src.models.db_models import User
# from .user_schemas import UserRead

class CommentRead(BaseModel):
    id: int
    user_id: int
    post_id: int
    reply_id: int | None
    text: str
    comment_vote_total: int | None
    user: User 

    replies: list["CommentRead"]
    comment_votes: list[VoteRead]

class CommentCreate(BaseModel):
    user_id: int | None
    post_id: int | None
    text: str

class ReplyCreate(BaseModel):
    user_id: int | None
    post_id: int | None
    reply_id: int | None
    text: str

class CommentEdit(BaseModel):
    text: str