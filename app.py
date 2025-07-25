from fastapi import APIRouter, FastAPI, Request, Depends, HTTPException, Form, Body
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from models.users import UserDB
from routers.auth_routes import auth_router
from schemas.users import User
from security import get_current_user, require_role
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

from models.users import Base
Base.metadata.create_all(bind=engine)

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