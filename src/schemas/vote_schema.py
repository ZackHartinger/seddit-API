from pydantic import BaseModel

class VoteRead(BaseModel):
    id: int
    user_id: int
    post_id: int
    comment_id: int

class VoteCreate(BaseModel):
    user_id: int
    post_id: int
    comment_id: int