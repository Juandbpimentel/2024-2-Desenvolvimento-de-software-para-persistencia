from pydantic import BaseModel, Field
from typing import List, Optional


class Classe(BaseModel):
    id: Optional[int] = Field(default=None)
    nome: str
    descricao: str
    escala_dano_por_nivel: int
    escala_vida_por_nivel: int
    escala_mana_por_nivel: int
    personagens: List['Personagem'] = Field(default_factory=list)
    skills: List['Skill'] = Field(default_factory=list)

class Skill(BaseModel):
    id: Optional[int] = Field(default=None)
    nome: str
    descricao: str
    nivel_necessario: int
    dano_base_da_skill: Optional[int] = None
    cura_base_da_skill: Optional[int] = None
    custo_de_mana_base: Optional[int] = None
    custo_de_vida_base: Optional[int] = None
    classe_id: int
    classe: Optional['Classe'] = None

class Personagem(BaseModel):
    id: Optional[int] = Field(default=None)
    nome: str
    nivel: int
    poder: int
    xp_atual: int
    xp_proximo_nivel: int
    hp_atual: int
    hp_max: int
    mana_atual: int
    mana_max: int
    forca: int
    defesa: int
    classe_id: int
    guilda_id: Optional[int] = None
    classe: Optional['Classe'] = None
    guilda: Optional['Guilda'] = None
    skills: List['Skill'] = Field(default_factory=list)

class Guilda(BaseModel):
    id: Optional[int] = Field(default=None)
    nome: str
    descricao: str
    dono_id: Optional[int] = None
    dono: Optional['Personagem'] = None
    personagens: List['Personagem'] = Field(default_factory=list)