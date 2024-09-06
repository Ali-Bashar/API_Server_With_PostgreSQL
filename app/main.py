from app.routers import auth
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .routers import vote, comments
from fastapi import FastAPI
from .database import engine
from sqlalchemy.orm import Session
from .routers import items, users, posts
from .config import Settings

settings = Settings() 

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(items.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(vote.router)
app.include_router(comments.router)

@app.get("/")
def root():
    return {"message":"Hello world"}
     

