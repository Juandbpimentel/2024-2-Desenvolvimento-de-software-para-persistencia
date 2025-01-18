from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import SQLModel, Field
from typing import Optional


class Membro(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: str
    senha: str


Base = declarative_base()
class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer,primary_key=True, index=True)
    email = Column(String, unique=True)
    nome = Column(String)
    senha = Column(String)
