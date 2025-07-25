from sqlalchemy import Column, ForeignKey, Integer, String, Table
from database import Base
from sqlalchemy.orm import relationship

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

    ingredients = relationship("Ingredient", secondary="recipe_ingredients", backref="recipes")

recipe_ingredients = Table(
    "recipe_ingredients",
    Base.metadata,
    Column("recipe_id", ForeignKey("recipes.id"), primary_key=True),
    Column("ingredient_id", ForeignKey("ingredients.id"), primary_key=True)
)