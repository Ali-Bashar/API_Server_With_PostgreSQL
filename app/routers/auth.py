from fastapi import APIRouter, Depends, HTTPException, status, Response
from .. import database, schemas, models, utils
from . import Oauth2
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(tags=['Authentication'],prefix="/login")

@router.post('/')
def login(user_credantials: OAuth2PasswordRequestForm = Depends(),
           db: Session=Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.user_name == user_credantials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid credantials")
    
    if not utils.verify(plain_password=user_credantials.password,hashed_password=user.user_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invelid credantials")
    
    access_token = Oauth2.create_access_token(data={"user_id": user.user_id})

    return {'access token': access_token, "token_type": "bearer"}