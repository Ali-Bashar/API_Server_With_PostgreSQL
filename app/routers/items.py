from .. import models,schemas
from .Oauth2 import get_current_user
from ..database import get_db
from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/items",tags=['Item'])

@router.get('/',response_model=List[schemas.ResponseItem])
def get_items(db:Session = Depends(get_db)):
    items = db.query(models.Items).all()

    return items

@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ResponseItem)
def get_item(id:int,db:Session = Depends(get_db)):
    try:
        items = db.query(models.Items).filter(models.Items.id == id).first()

        if items == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Id: {id} was not found")
        
        return items
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Error: {e}")


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.ResponseItem)
def create_item(item: schemas.Create_item,db:Session = Depends(get_db), get_current_user:int=Depends(get_current_user)):
    try:
        new_item = models.Items(**item.dict())
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        
        return  new_item
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Error: {e}")    

@router.put("/{id}",response_model=schemas.ResponseItem)
def Update_item(id:int,item: schemas.Update_item,db: Session=Depends(get_db)):
    try:
        item_query = db.query(models.Items).filter(models.Items.id == id)
        items = item_query.first()
        
        if items == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Item with id: {id} not found")
        
        item_query.update(item.dict(),synchronize_session=False)
        db.commit()

        return item_query.first()
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Error: {e}")
    
@router.delete("/{id}")
def Delete_item(id:int,db: Session=Depends(get_db)):
    try:
        item = db.query(models.Items).filter(models.Items.id == id)

        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Item with id : {id} not found")
        
        item.delete(synchronize_session=False)
        db.commit()

        return {"status":"successful"}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Error: {e}")