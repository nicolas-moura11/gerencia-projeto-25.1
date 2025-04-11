from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from sqlalchemy.orm import relationship

from database import Base


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

class UserRegistration(BaseModel):
    username: str
    email: str
    password: str

    role: str


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)
    role = Column(String, default="client")

    recipes = relationship("RecipeDB", back_populates="creator")  # Relacionamento com as receitas


class Recipe(BaseModel):
    id: Optional[int] = None  # O id pode ser None, pois será atribuído pelo banco de dados
    title: str
    ingredients: str
    preparation: str
    time: int
    image_filename: Optional[str] = None
    is_visible: bool = True

    class Config:
        orm_mode = True

class RecipeDB(Base):
    __tablename__ = "receitas"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    ingredients = Column(String, nullable=False)
    preparation = Column(String, nullable=False)
    time = Column(Integer, nullable=False)
    image_filename = Column(String, nullable=True)
    is_visible = Column(Boolean, default=True)  # Adicionando o campo de visibilidade
    creator_id = Column(Integer, ForeignKey("users.id"))  # Relacionando com o criador (usuário)

    creator = relationship("UserDB", back_populates="recipes")  # Relacionamento com a tabela de usuários


class RecipeResponse(BaseModel):
    id: int
    title: str
    ingredients: str
    preparation: str
    time: int
    image_filename: Optional[str] = None
    is_visible: Optional[bool] = True  # se você estiver usando esse campo

    class Config:
        orm_mode = True

