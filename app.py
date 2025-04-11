import os
from datetime import datetime

from fastapi import FastAPI, Request, Depends, HTTPException, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel

from typing import List, Optional, Annotated

from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Recipe, User, UserDB, RecipeDB, RecipeResponse

from routers.auth_routes import auth_router
from security import get_current_user, require_role


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ou especifique sua origem, tipo http://127.0.0.1:5500
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  # Isso é ESSENCIAL para aceitar o Authorization
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

@app.get("/users/me/", response_class=HTMLResponse)
async def read_users_me(current_user = Depends(get_current_user)):
    return {"username": current_user.username}

@app.get("/auth", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("authentication.html", {"request": request})

@app.get("/home", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# @app.get("/register-page", response_class=HTMLResponse)
# async def read_register_page(request: Request):
#     return templates.TemplateResponse("register-page.html", {"request": request})

@app.get("/users", response_model=List[User])

async def list_users(db: db_dependency):
    return db.query(UserDB).all()

@app.post("/receitas/", response_model=RecipeResponse)
async def criar_receita(
        title: str = Form(...),
        ingredients: str = Form(...),
        preparation: str = Form(...),
        time: int = Form(...),
        image: Optional[UploadFile] = File(None),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),  # Garantir que seja um criador
):
    image_filename = None
    if image:
        image_filename = f"static/imgs/{image.filename}"
        with open(image_filename, "wb") as buffer:
            buffer.write(await image.read())

    nova_receita = RecipeDB(
        title=title,
        ingredients=ingredients,
        preparation=preparation,
        time=time,
        image_filename=image_filename,
        creator_id=current_user.id,  # Associando a receita ao criador
    )

    db.add(nova_receita)
    db.commit()
    db.refresh(nova_receita)

    return nova_receita

@app.put("/receitas/{recipe_id}", response_model=Recipe)
async def editar_receita(
        recipe_id: int,
        title: Optional[str] = None,
        ingredients: Optional[str] = None,
        preparation: Optional[str] = None,
        time: Optional[int] = None,
        image: Optional[UploadFile] = None,
        is_visible: Optional[bool] = None,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),  # Garantir que seja o criador
):
    receita = db.query(RecipeDB).filter(RecipeDB.id == recipe_id).first()

    if not receita:
        raise HTTPException(status_code=404, detail="Receita não encontrada")

    if receita.creator_id != current_user.id:  # Verificar se o criador da receita é o usuário
        raise HTTPException(status_code=403, detail="Você não tem permissão para editar esta receita")

    # Atualizar os campos da receita
    if title:
        receita.title = title
    if ingredients:
        receita.ingredients = ingredients
    if preparation:
        receita.preparation = preparation
    if time:
        receita.time = time
    if image:
        image_filename = f"static/imgs/{image.filename}"
        with open(image_filename, "wb") as buffer:
            buffer.write(await image.read())
        receita.image_filename = image_filename
    if is_visible is not None:
        receita.is_visible = is_visible

    db.commit()
    db.refresh(receita)

    return receita


@app.get("/receitas/", response_model=List[RecipeResponse])
async def listar_receitas(db: Session = Depends(get_db)):
    return db.query(RecipeDB).filter(RecipeDB.is_visible == True).all()  # Mostrar apenas as visíveis


@app.get("/receitas/{recipe_id}", response_model=Recipe)
async def ver_receita(recipe_id: int, db: Session = Depends(get_db)):
    receita = db.query(RecipeDB).filter(RecipeDB.id == recipe_id).first()

    if not receita or not receita.is_visible:
        raise HTTPException(status_code=404, detail="Receita não encontrada ou não visível")

    return receita



@app.get("/admin-page", response_class=HTMLResponse, dependencies=[Depends(require_role("creator"))])
def admin_page(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

