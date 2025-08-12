from pydantic import BaseModel
from typing import Literal

class VoteRead(BaseModel):
    id: int
    user_id: int  
    vote_value: int

class PostVoteRead(VoteRead):
    post_id: int

class CommentVoteRead(VoteRead):
    comment_id: int

class PostVoteCreate(BaseModel):
    user_id: int
    post_id: int
    vote_value: Literal[-1, 1]

class CommentVoteCreate(BaseModel):
    user_id: int
    comment_id: int
    vote_value: Literal[-1, 1]