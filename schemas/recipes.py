from typing import List, Optional
from pydantic import BaseModel, ConfigDict


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