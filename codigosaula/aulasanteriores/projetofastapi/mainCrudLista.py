from typing import Union, List
from http import HTTPStatus
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel


app = FastAPI()

class Item(BaseModel):
    id: int
    nome: str
    valor: float
    is_oferta: Union[bool, None] = None

itens_db: List[Item] = []


@app.get("/hi", status_code=HTTPStatus.OK)
async def helloWorld():
    return {"msg": "Hello World!"}


@app.get("/itens/{item_id}", status_code=HTTPStatus.OK, response_model=Item)
def lerItem(item_id: int):
    for indice,item_atual in enumerate(itens_db):
        if item_atual.id == item_id:
            return item_atual
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND,detail='Item não encontrado')

@app.get("/itens/", response_model=List[Item])
def listarItens():
    return itens_db

@app.post("/itens/",response_model=Item, status_code=HTTPStatus.CREATED)
def adicionarItem(item: Item):
    if any(item.id == item_atual.id for item_atual in itens_db):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Já existe um item com esse ID no sistema.")
    itens_db.append(item)
    return item

@app.put("/itens/{item_id}", response_model=Item, status_code=HTTPStatus.OK)
def atualizarItem(item_id: int,item_atualizado: Item):
    for indice,item_atual in enumerate(itens_db):
        if item_id == item_atual.id:
            if item_atualizado.id != item_id:
                item_atualizado.id = item_id
            itens_db[indice] = item_atualizado
            return item_atualizado        
    raise 

@app.delete("/itens/{item_id}", response_model=Item, status_code=HTTPStatus.OK)
def removerItem(item_id: int):
    for indice,itemAtual in enumerate(itens_db):
        if itemAtual.id == item_id:
            item = itens_db.pop(indice)
            return item
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Não existe um item com esse ID no sistema.")