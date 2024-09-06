from multiprocessing import synchronize
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import HttpUrl
from sqlalchemy.orm import Session
from .. import database, models, schemas
from . import Oauth2

router = APIRouter(tags=['comments'], prefix='/comments')

@router.post('/')
def commenting(comment:schemas.Comments,db:Session=Depends(database.get_db),
               current_user: str = Depends(Oauth2.get_current_user)):
    
    post_id = db.query(models.Post).filter(models.Post.post_id == comment.post_id).first()

    if not post_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post id {comment.post_id} was not found")
    
    comment_query = db.query(models.Comment).filter(models.Comment.post_id == comment.post_id, models.Comment.user_id == current_user.user_id)

    comment_found = comment_query.first()

    if comment_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"User with user id:{current_user.user_id} posted comment already")
    
    new_comment = models.Comment(
    comment=comment.comment,
    post_id=comment.post_id,
    user_id=current_user.user_id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)


    return {"message":"successfully added comment"}
