from multiprocessing import synchronize
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import HttpUrl
from sqlalchemy.orm import Session
from .. import database, models, schemas
from . import Oauth2

router = APIRouter(tags=['comments'], prefix='/comments')

router.post('/')
def commenting(db:Session=Depends(database.get_db)):
    pass