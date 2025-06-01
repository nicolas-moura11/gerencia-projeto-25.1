from typing import List, Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Table, UniqueConstraint
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

    likes = relationship("Curtida", back_populates="user")

    #shopping_list = relationship("ShoppingListItem", back_populates="user", cascade="all, delete-orphan")


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    image_url = Column(String, nullable=True)

    likes = relationship("Curtida", back_populates="recipe")
    ingredients = relationship("Ingredient", secondary="recipe_ingredients", backref="recipes")


recipe_ingredients = Table(
    "recipe_ingredients",
    Base.metadata,
    Column("recipe_id", ForeignKey("recipes.id"), primary_key=True),
    Column("ingredient_id", ForeignKey("ingredients.id"), primary_key=True)
)


class IngredientBase(BaseModel):
    name: str


class IngredientResponse(IngredientBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class RecipeCreate(BaseModel):
    title: str
    description: str
    ingredients: List[str]  # apenas os nomes
    image_url: Optional[str] = None


class RecipeResponse(BaseModel):
    id: int
    title: str
    description: str
    image_url: Optional[str]
    ingredients: List[IngredientResponse]

    model_config = ConfigDict(from_attributes=True)

class Curtida(Base):
    __tablename__ = "curtidas"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    recipe_id = Column(Integer, ForeignKey("recipes.id"))

    user = relationship("UserDB", back_populates="likes")
    recipe = relationship("Recipe", back_populates="likes")

    __table_args__ = (
        # Garante que um usuário curta uma receita só uma vez
        UniqueConstraint("user_id", "recipe_id", name="unique_user_recipe"),
    )

class CurtidaResponse(BaseModel):
    recipe_id: int
    user_id: int
    curtido: bool

    model_config = ConfigDict(from_attributes=True)


'''class ShoppingListItem(Base):
    __tablename__ = "shopping_list_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ingredient = Column(String, nullable=False)
    quantity = Column(String, nullable=True)

    user = relationship("UserDB", back_populates="shopping_list")


class ShoppingListItemCreate(BaseModel):
    ingredient: str
    quantity: str | None = None

class ShoppingListItemRead(ShoppingListItemCreate):
    id: int
    class Config:
        from_attributes = True
'''

class PasswordReset(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


fake_users_db = {}