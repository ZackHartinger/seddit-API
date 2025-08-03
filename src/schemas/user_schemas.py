from pydantic import BaseModel
from .comment_schema import CommentRead
from .post_schemas import PostRead
from .vote_schema import VoteRead

class UserRead(BaseModel) :
    id: int
    user_name: str
    email: str

    posts: list[PostRead]
    user_comments: list[CommentRead]
    user_votes: list[VoteRead]