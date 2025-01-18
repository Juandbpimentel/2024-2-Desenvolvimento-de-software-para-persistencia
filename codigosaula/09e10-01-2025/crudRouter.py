from fastapi_crudrouter import SQLAlchemyCRUDRouter
from models import Usuario
from database import get_db
from pydantic import BaseModel


class UsuarioSchema(BaseModel):
    id: int
    nome: str
    email: str
    senha: str

    class Config:
        orm_mode = True


router = SQLAlchemyCRUDRouter(
    schema = UsuarioSchema,
    db_model=Usuario,
    db=get_db,
    prefix='usuario'
)
