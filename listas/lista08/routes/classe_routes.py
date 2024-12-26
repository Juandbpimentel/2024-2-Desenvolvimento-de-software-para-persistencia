from fastapi import APIRouter, HTTPException
from typing import List
from models import Classe
from models import Personagem
from models import Skill
from repositories.classe_repository import (
    create_classe,
    get_classe,
    update_classe,
    delete_classe,
    get_all_classes,
    get_skills,
    get_personagens_with_classe,
)

router = APIRouter(
    prefix="/classes",
    tags=["classes"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=Classe)
def create_new_classe(classe: Classe):
    classe_id = create_classe(classe)
    return get_classe(classe_id)

@router.get("/{classe_id}", response_model=Classe)
def read_classe(classe_id: int):
    classe = get_classe(classe_id)
    if classe is None:
        raise HTTPException(status_code=404, detail="Classe not found")
    return classe

@router.put("/{classe_id}", response_model=Classe)
def update_existing_classe(classe_id: int, update_data: dict):
    if not update_classe(classe_id, update_data):
        raise HTTPException(status_code=404, detail="Classe not found")
    return get_classe(classe_id)

@router.delete("/{classe_id}", response_model=bool)
def delete_existing_classe(classe_id: int):
    if not delete_classe(classe_id):
        raise HTTPException(status_code=404, detail="Classe not found")
    return True

@router.get("/", response_model=List[Classe])
def read_all_classes():
    return get_all_classes()

@router.get("/{classe_id}/skills", response_model=List[Skill])
def read_skills_from_classe(classe_id: int):
    return get_skills(classe_id)

@router.get("/{classe_id}/personagens", response_model=List[Personagem])
def read_personagens_with_classe(classe_id: int):
    return get_personagens_with_classe(classe_id)