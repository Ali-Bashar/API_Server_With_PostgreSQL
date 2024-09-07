import email
from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP,text, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

class Items(Base):
    __tablename__ = 'MyItems'

class Post(Base):
    __tablename__ = 'posts'
    post_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    comments = relationship("Comment", back_populates="post")

class Post(Base):
    __tablename__ = "Posts"
    post_id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default=text("True"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),server_default=text('NOW()'),nullable=False)
    owner_id = Column(Integer, ForeignKey("User.user_id", ondelete="CASCADE"),nullable=False)
    owner = relationship("User")

class User(Base):
    __tablename__ = "User"

    user_id = Column(Integer,primary_key=True,nullable=False)
    user_name = Column(String,nullable=False)
    user_password = Column(String,nullable=False)
    email = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True),server_default=text('NOW()'),nullable=False)
    phone_number = Column(String)

class Vote(Base):
    __tablename__ = "Vote"
    user_id = Column(Integer, ForeignKey("User.user_id", ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer, ForeignKey("Posts.post_id", ondelete="CASCADE"),primary_key=True)


class Comment(Base):
    __tablename__ = 'comments'

    comment_id = Column(Integer, primary_key=True, index=True)
    comment = Column(String)
    post_id = Column(Integer, ForeignKey('posts.post_id'))
    post = relationship("Post", back_populates="comments")


