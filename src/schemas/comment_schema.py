from pydantic import BaseModel
from .vote_schema import VoteRead

class CommentRead(BaseModel):
    id: int
    user_id: int
    post_id: int
    reply_id: int | None
    text: str

    replies: list["CommentRead"]
    comment_votes: list[VoteRead]

class CommentCreate(BaseModel):
    user_id: int | None
    post_id: int | None
    reply_id: int | None
    text: str