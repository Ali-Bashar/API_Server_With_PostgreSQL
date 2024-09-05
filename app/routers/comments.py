from multiprocessing import synchronize
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import HttpUrl
from sqlalchemy.orm import Session
from .. import database, models, schemas
from . import Oauth2

router = APIRouter(tags=['comments'], prefix='/comments')

router.post('/')
def commenting(comment:schemas.Comments,db:Session=Depends(database.get_db),
               current_user: str = Depends(Oauth2.get_current_user)):
    
    post_id = db.query(models.Post).filter(models.Post.post_id == comment.post_id).first()

    if not post_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post id {comment.post_id} was not found")