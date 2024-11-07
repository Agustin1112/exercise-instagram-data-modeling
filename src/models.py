from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Text, create_engine
from sqlalchemy.orm import relationship, declarative_base
from eralchemy import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    posts = relationship("Post", back_populates="user")
    followers = relationship("Follower", foreign_keys='Follower.user_to_id')
    following = relationship("Follower", foreign_keys='Follower.user_from_id')
    comments = relationship("Comment", back_populates="author")

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="posts")
    media = relationship("Media", back_populates="post")
    comments = relationship("Comment", back_populates="post")

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(Enum('image', 'video', name='media_type'), nullable=False)
    url = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    post = relationship("Post", back_populates="media")

class Follower(Base):
    __tablename__ = 'follower'
    user_from_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user_to_id = Column(Integer, ForeignKey('user.id'), primary_key=True)

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

# Creo el motor de base de datos
engine = create_engine('sqlite:///instagram.db')

# Creo todas las tablas en la base de datos
Base.metadata.create_all(engine)

# Genero el diagrama en diagram.png
try:
    render_er(Base, 'diagram.png')
    print("Diagrama generado exitosamente en diagram.png")
except Exception as e:
    print("Ocurrió un error al generar el diagrama:", e)




