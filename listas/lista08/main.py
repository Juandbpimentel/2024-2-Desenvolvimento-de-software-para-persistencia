from contextlib import asynccontextmanager
from typing import List, Dict, Optional
from http import HTTPStatus
from fastapi import FastAPI
import logging


from logging_config import setup_logging
from database import create_db_and_tables
from routes.classe_routes import router as classe_router

@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    setup_logging()
    create_db_and_tables()
    logging.info("Iniciando a aplicação")
    yield
    logging.info("Finalizando a aplicação")

app = FastAPI(
    lifespan=lifespan
)

app.include_router(classe_router)

@app.get(
    "/",
    status_code=HTTPStatus.CREATED,
    description="Endpoint de exemplo",
    summary="Exemplo",
)
async def exemplo_endpoint() -> Dict[str, int | str | Dict[str, bool | str]]:
    logging.info("Endpoint de exemplo chamado")
    return {
        "quantidade": 0,
        "status": "ok",
        "mensagem": "",
        "erro": {"status": False, "mensagem": ""},
    }