from fastapi import APIRouter, FastAPI, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from routers.auth_routes import auth_router
from security import get_current_user, require_role
from models import Recipe, User, UserDB, ShoppingListItem, ShoppingListItemRead, ShoppingListItemCreate
from pydantic import BaseModel
from typing import List, Annotated
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from routers import recipes

app = FastAPI()
app.include_router(recipes.router)
router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from models import Base
Base.metadata.create_all(bind=engine)

# # Schemas Pydantic
# class RecipeBase(BaseModel):
#     title: str
#     description: str

# class RecipeCreate(RecipeBase):
#     post_time: datetime = datetime.now()

# class RecipeResponse(RecipeBase):
#     id: int
#     post_time: datetime
#     class Config:
#         orm_mode = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(auth_router)

# @app.get("/users/me/", response_class=HTMLResponse)
# async def read_users_me(current_user = Depends(get_current_user)):
#     return {"username": current_user.username}

@app.get("/auth", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("authentication.html", {"request": request})

@app.get("/home", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/users", response_model=List[User])
async def list_users(db: db_dependency):
    return db.query(UserDB).all()

@app.get("/receitas-page", response_class=HTMLResponse)
def receitas_page(request: Request):
    return templates.TemplateResponse("recipes.html", {"request": request})

@app.get("/auth/status")
async def auth_status(user: User = Depends(get_current_user)):
    return {"is_authenticated": True}

@app.get("/shopping-list")
def view_shopping_list(request: Request, db: Session = Depends(get_db), user = Depends(get_current_user)):
    items = db.query(ShoppingListItem).filter_by(user_id=user.id).all()
    return templates.TemplateResponse("shopping_list.html", {"request": request, "shopping_list": items})

@app.post("/shopping-list")
def add_item_html(request: Request, ingredient: str = Form(...), quantity: str = Form(None),
                  db: Session = Depends(get_db), user = Depends(get_current_user)):
    item = ShoppingListItem(ingredient=ingredient, quantity=quantity, user_id=user.id)
    db.add(item)
    db.commit()
    return RedirectResponse(url="/shopping-list", status_code=303)

@app.post("/shopping-list/delete/{item_id}")
def remove_item_html(item_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    item = db.query(ShoppingListItem).filter_by(id=item_id, user_id=user.id).first()
    if item:
        db.delete(item)
        db.commit()
    return RedirectResponse(url="/shopping-list", status_code=303)

@app.post("/shopping-list/from-recipe/{recipe_id}")
def add_from_recipe(recipe_id: int, ingredients: List[str] = Form(...),
                    db: Session = Depends(get_db), user = Depends(get_current_user)):
    for ing in ingredients:
        item = ShoppingListItem(ingredient=ing, quantity=None, user_id=user.id)
        db.add(item)
    db.commit()
    return RedirectResponse(url="/shopping-list", status_code=303)


@router.get("/me")
def get_user_info(user = Depends(get_current_user)):
    return {
        "username": user.username,
        "role": user.role
    }

app.include_router(router)

@auth_router.get("/reset-password", response_class=HTMLResponse)
def show_reset_form(request: Request, token: str):
    return templates.TemplateResponse("reset_password_form.html", {"request": request, "token": token})