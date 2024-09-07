from . import schemas
from typing import Optional
from pydantic import BaseModel,EmailStr
import datetime
from pydantic.types import conint
from typing import Optional, List

class Item(BaseModel):
    item_name:str
    item_price:float
    sale:bool=False

class Create_item(Item):
    pass

class Update_item(Item):
    pass


class ResponseItem(BaseModel):
    item_name:str
    item_price:float
    sale:bool
    id:int

    class Confiq:
        from_attribute = True


class CreateUser(BaseModel):
    email:EmailStr
    user_name:str
    user_password:str


class UserOut(BaseModel):
    user_id:str
    email:str
    user_id:int
    created_at:datetime

    class Config:
        from_attribute = True
        arbitrary_types_allowed = True


class UserCrentials(BaseModel):
    email:EmailStr
    user_password:str


class AccessToken(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[int] = None

class PostBase(BaseModel):
    content:str
    title:str
    published:Optional[bool] = True

class CreatePost(PostBase):
    pass

class UpdatePost(PostBase):
    pass

class PostOut(BaseModel):
    post_id: int
    title: str
    content: str
    owner: UserOut  # Nested Pydantic model

    class Config:
        orm_mode = True


class CommentOut(BaseModel):
    comment_id: str
    comment: str
    user_id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True

class PostOutWithVotesAndComments(BaseModel):
    post: PostOut
    votes: int
    comments: List[CommentOut] = []

    class Config:
        orm_mode = True

class Vote(BaseModel):
    post_id:int
    dir: int =conint(le=1)

class PostOutWithVotes(BaseModel):
    Post: schemas.PostOut
    Votes: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


