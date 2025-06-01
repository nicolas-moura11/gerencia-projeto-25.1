from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Annotated
from models import Curtida, Recipe, UserDB, CurtidaResponse
from security import get_current_user, get_db

router = APIRouter(
    prefix="/receitas",
    tags=["curtidas"]
)

@router.post(
    "/{recipe_id}/curtir",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Curtida atualizada com sucesso"},
        404: {"description": "Receita não encontrada"},
        401: {"description": "Não autorizado"}
    }
)
def curtir_ou_descurtir(
        recipe_id: int,
        current_user: Annotated[UserDB, Depends(get_current_user)],
        db: Session = Depends(get_db)
):
    """
    Alterna o estado de curtida de uma receita.
    - Se o usuário já curtiu, remove a curtida
    - Se não curtiu, adiciona uma nova curtida
    Retorna o novo estado e o total de curtidas
    """
    # Verifica se a receita existe
    receita = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not receita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receita não encontrada"
        )

    # Verifica curtida existente
    curtida = db.query(Curtida).filter(
        Curtida.user_id == current_user.id,
        Curtida.recipe_id == recipe_id
    ).first()

    if curtida:
        # Remove curtida existente
        db.delete(curtida)
        action = "curtida removida"
    else:
        # Adiciona nova curtida com timestamp
        nova_curtida = Curtida(
            user_id=current_user.id,
            recipe_id=recipe_id,
            data_curtida=datetime.utcnow()
        )
        db.add(nova_curtida)
        action = "curtida adicionada"

    db.commit()

    # Obtém contagem atualizada
    total_curtidas = db.query(Curtida).filter_by(recipe_id=recipe_id).count()

    return {
        "status": "success",
        "action": action,
        "curtido": not curtida,  # Inverte o estado atual
        "total_curtidas": total_curtidas,
        "user_id": current_user.id,
        "recipe_id": recipe_id
    }

@router.get(
    "/{recipe_id}/curtidas",
    responses={
        200: {"description": "Quantidade de curtidas retornada com sucesso"},
        404: {"description": "Receita não encontrada"}
    }
)
def get_qtd_curtidas(
        recipe_id: int,
        db: Session = Depends(get_db)
):
    """
    Retorna a quantidade total de curtidas para uma receita
    """
    if not db.query(Recipe).filter_by(id=recipe_id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receita não encontrada"
        )

    qtd = db.query(Curtida).filter_by(recipe_id=recipe_id).count()
    return {"total_curtidas": qtd}

@router.get(
    "/{recipe_id}/status",
    response_model=CurtidaResponse,
    responses={
        200: {"description": "Status de curtida obtido com sucesso"},
        404: {"description": "Receita não encontrada"},
        401: {"description": "Não autorizado"}
    }
)
def verificar_status_curtida(
        recipe_id: int,
        current_user: Annotated[UserDB, Depends(get_current_user)],
        db: Session = Depends(get_db)
):
    """
    Verifica se o usuário atual curtiu a receita
    Retorna o status de curtida e informações básicas
    """
    if not db.query(Recipe).filter_by(id=recipe_id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receita não encontrada"
        )

    like = db.query(Curtida).filter(
        Curtida.user_id == current_user.id,
        Curtida.recipe_id == recipe_id
    ).first()

    return {
        "recipe_id": recipe_id,
        "user_id": current_user.id,
        "curtido": like is not None,
    }