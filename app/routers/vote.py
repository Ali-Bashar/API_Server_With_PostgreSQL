from multiprocessing import synchronize
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import HttpUrl
from sqlalchemy.orm import Session
from .. import database, models, schemas
from . import Oauth2

router = APIRouter(prefix="/vote",tags=["Vote"])

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote : schemas.Vote, db: Session = Depends(database.get_db),
         current_user: str = Depends(Oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.post_id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {vote.post_id} does not exist")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.user_id)
    
    found_vote =  vote_query.first()
    
    if (vote.dir==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"User:{current_user.user_id} already voted on post {vote.post_id}")
        
        new_vote = models.Vote(post_id = vote.post_id,user_id = current_user.user_id)
        db.add(new_vote)
        db.commit()

        return {"message":"successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Vote not found")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message":"successfully deleted"}