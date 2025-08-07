from pydantic import BaseModel
from datetime import datetime
from .comment_schema import CommentRead
from .vote_schema import VoteRead

class PostRead(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    title: str
    description: str
    post_vote_total: int | None

    post_comments: list[CommentRead]
    post_votes: list[VoteRead]

class PostCreate(BaseModel):
    user_id: int
    title: str
    description: str