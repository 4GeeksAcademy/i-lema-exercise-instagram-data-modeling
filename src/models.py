import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class Follower(Base):
    __tablename__ = 'follower'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    user_from_id = Column(Integer, ForeignKey('user.ID'), primary_key=True)
    user_to_id = Column(Integer, ForeignKey('user.ID'), primary_key=True)    

class User(Base):
    __tablename__ = 'user'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    ID = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    firstname = Column(String(250), nullable=False)
    lastname = Column(String(250), unique=True, nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    comment = relationship('Comment', backref='user', lazy=True)
    post = relationship('Post', backref='user', lazy=True)
    followed = relationship(
        'User',
        secondary=Follower,
        primaryjoin=(Follower.user_from_id == id),
        secondaryjoin=(Follower.user_to_id == id),
        backref='following',
        lazy='dynamic')

class Comment(Base):
    __tablename__ = 'comment'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    ID = Column(Integer, primary_key=True)
    comment_text = Column(String(250), nullable=False)
    author_id = Column(Integer, ForeignKey('user.ID'))
    post_id = Column(Integer, ForeignKey('user.ID'))

class Post(Base):
    __tablename__ = 'post'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    ID = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.ID'))
    user = relationship(User)
    comment = relationship('Comment', backref='post', lazy=True)
    media = relationship('Media', backref='post', lazy=True)

class Media(Base):
    __tablename__ = 'media'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute
    ID = Column(Integer, primary_key=True)
    type = Column(Enum("Vídeo","Foto","Reel"))
    url = Column(String(250), nullable=False)
    post_id = Column(Integer, ForeignKey('post.ID'))

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e