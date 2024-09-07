from operator import contains
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import func
from .. import database, models, schemas
from . import Oauth2
from sqlalchemy.orm import aliased
from sqlalchemy.orm import Session
from typing import List, Optional


router = APIRouter(tags=["Posts"], prefix="/posts")

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.PostOutWithVotesAndComments])
def get_posts(db: Session = Depends(database.get_db),
              limit: int = 100, skip: int = 0, search: Optional[str] = ""):
    
    # Create an alias for the Comment model
    commentAlias = aliased(models.Comment)

    posts = db.query(
    models.Post,
    func.count(models.Vote.post_id).label("Votes"),
    func.array_agg(func.json_build_object(
        'comment', commentAlias.comment,
        'user_id', commentAlias.user_id,
        'created_at', commentAlias.created_at
    )).filter(commentAlias.comment != None).label('comments')  # Avoid null comments
).outerjoin(
    models.Vote, models.Vote.post_id == models.Post.post_id, isouter=True
).outerjoin(
    commentAlias, commentAlias.post_id == models.Post.post_id, isouter=True
).group_by(
    models.Post.post_id
).filter(
    models.Post.title.ilike(f"%{search}%")
).limit(limit).offset(skip).all()




@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.PostOutWithVotesAndComments)
def get_post_id(id:int,db: Session=Depends(database.get_db),
                 current_user : str = Depends(Oauth2.get_current_user)):
    
    posts_votes = db.query(
                models.Post, func.count(models.Vote.post_id).label("Votes")
            ).join(
                models.Vote,models.Vote.post_id == models.Post.post_id,isouter=True
            ).group_by(
                models.Post.post_id
            ).filter(models.Post.post_id == id).first()
    
    post, votes = posts_votes

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No post wiith id:{id} exist")
    
    if post.owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User is not autharised")
    
    return {"Post":post,"Votes":votes}

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostOut)
def create_post(post:schemas.CreatePost, db: Session=Depends(database.get_db),
                current_user: str = Depends(Oauth2.get_current_user)):
    
    created_post = models.Post(owner_id = current_user.user_id,**post.dict())
    db.add(created_post)
    db.commit()
    db.refresh(created_post)

    return created_post

@router.put("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.PostOut)
def update_post(id:int, post: schemas.UpdatePost,db: Session=Depends(database.get_db),
                current_user: str = Depends(Oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.post_id == id)
    posts = post_query.first()
    
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post woth id:{id} not found")
    
    if posts.owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User is not autharised")
    
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()

    return post_query.first()

@router.delete("/{id}",status_code=status.HTTP_200_OK)
def delete_post(id:int, db: Session=Depends(database.get_db),
                current_user:str=Depends(Oauth2.get_current_user)):
    
    query = db.query(models.Post).filter(models.Post.post_id == id)
    query_post = query.first()
    if not query_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id:{id} not found")
    
    if query_post.owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User is not autharised")

    query.delete(synchronize_session=False)
    db.commit()

    return {"Status":f"successfuly deleted post with id:{id}"}