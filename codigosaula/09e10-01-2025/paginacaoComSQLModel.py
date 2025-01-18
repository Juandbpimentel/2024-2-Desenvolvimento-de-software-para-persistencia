from typing import List, Optional, Dict, Any

from fastapi.params import Depends, Query
from sqlmodel import SQLModel, Session, select
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, func
from models import Membro

app = FastAPI()

DATABASE_URL = "postgresql://postgres:pgpass@localhost:5432/persistencia"
engine = create_engine(DATABASE_URL, echo=True)


@app.on_event("startup")
def startup():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


@app.post("/membros", response_model=Membro)
def create_membro(membro: Membro, session: Session = Depends(get_session)):
    session.add(membro)
    session.commit()
    session.refresh(membro)
    return membro
    pass


@app.post("/membros/insertall")
def insert_all(membros: list[Membro], session: Session = Depends(get_session)):
    for membro in membros:
        session.add(membro)
    session.commit()
    session.refresh(membros)
    return {"status": "sucesso"}


@app.get("/membros/paginacao_com_last_id", response_model=List[Membro])
def list_membros(
        last_id: Optional[int] = Query(None),
        page_size: int = Query(10),
        session: Session = Depends(get_session)
):
    if last_id:
        query = select(Membro).where(Membro.id > last_id).limit(page_size)
    else:
        query = select(Membro).limit(page_size)
    membros = session.exec(query).all()
    return membros


@app.get("/membros/paginacao_com_offset")
def list_membros_paginados(
        offset: Optional[int] = Query(0, ge=0),
        limit: int = Query(10, ge=1),
        session: Session = Depends(get_session)
):
    # forma ruim total = session.execute(select(func.count(Membro.id))).scalar()
    total = session.exec(select(func.count(Membro.id))).one_or_none() or 0
    membros = session.exec(select(Membro).offset(offset).limit(limit)).all()
    current_page = (offset // limit) + 1
    if offset % limit != 0:
        current_page += 1
    total_pages = (total // limit)
    if total % limit != 0:
        total_pages += 1
    return {
        "data": membros,
        "pagination": {
            "total": total,
            "current_page": current_page,
            "total_pages": total_pages,
            "page_size": limit
        }
    }

@app.get("/membros/cursor", response_model=Dict[str,Any])
def list_membros_cursor(
        last_id: Optional[int] = Query(None),
        page_size: int = Query(10, ge=1),
        session: Session = Depends(get_session)
):
    if last_id:
        query = select(Membro).where(Membro.id > last_id).limit(page_size)
    else:
        query = select(Membro).limit(page_size)
    membros = session.exec(query).all()

    return {
        "data": membros,
        "pagination": {
            "last_id": membros[-1].id if membros else None,
            "page_size": page_size,
        }
    }


@app.get("/membros/filtrados", response_model=Dict[str,Any])
def list_membros_filtrados(
        nome: Optional[str] = Query(None),
        membro_id: Optional[int] = Query(None),
        email: Optional[str] = Query(None),
        offset: Optional[int] = Query(0,ge=0),
        limit: Optional[int] = Query(10,ge=1),
        session: Session = Depends(get_session)
):
    query = select(Membro)
    if nome:
        query = query.where(func.lower(Membro.nome).like(f"%{func.lower(nome)}%"))
    if membro_id:
        query = query.where(Membro.id == membro_id)
    if email:
        query = query.where(func.lower(Membro.email).like(f"%{func.lower(email)}%"))

    total = session.exec(select(func.count(Membro.id)).select_from(query.subquery())).one_or_none() or 0
    membros = session.exec(select(Membro).offset(offset).limit(limit)).all()
    current_page = (offset // limit) + 1
    if offset % limit != 0:
        current_page += 1
    total_pages = (total // limit)
    if total % limit != 0:
        total_pages += 1
    return {
        "data": membros,
        "pagination": {
            "total": total,
            "current_page": current_page,
            "total_pages": total_pages,
            "page_size": limit
        }
    }


