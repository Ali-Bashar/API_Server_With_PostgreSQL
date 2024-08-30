from secrets import token_urlsafe
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from .. import schemas, database, models
from ..config import settings
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encode_jwt = jwt.encode(claims=to_encode,key=SECRET_KEY,algorithm=ALGORITHM)

    return encode_jwt

def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token=token,key=SECRET_KEY,algorithms=[ALGORITHM])
        id:str = payload.get("user_id")
        
        if id == None:
            raise credentials_exception
    
        token_data = schemas.TokenData(id=id)
        return token_data
        
    except JWTError:
        raise credentials_exception
    
def get_current_user(token:str = Depends(oauth_scheme),db:Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials",headers={"WWW-Authenticate":"Bearer"})
    
    token_data = verify_access_token(token,credentials_exception=credentials_exception)

    user = db.query(models.User).filter(models.User.user_id == token_data.id).first()

    return user