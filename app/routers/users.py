from ..database import get_db
from .. import schemas,utils,models
from fastapi import Depends, HTTPException, status, FastAPI, APIRouter
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(prefix="/users",tags=['User'])

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def Create_user(user: schemas.CreateUser,db:Session=Depends(get_db)):
    try:
        # Hash the password
        hashed_password = utils.hash(user.user_password)
        user.user_password = hashed_password

        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return  new_user
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Error: {e}")    

@router.get('/',response_model=List[schemas.UserOut])
def get_user(db : Session = Depends(get_db)):
    
    try:
        users = db.query(models.User).all()

        return users
    
    except Exception as e:
        print("Error: ",e)


@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.UserOut)
def get_user_id(id:int, db: Session= Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.user_id == id).first()

        if not user:    
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"User with id {id} does not exist")
    
        return user
    
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Error: {e}")