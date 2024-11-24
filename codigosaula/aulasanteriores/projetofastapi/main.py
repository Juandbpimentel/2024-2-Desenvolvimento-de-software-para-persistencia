from typing import Union
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/itens/{item_id}")
def read_item(item_id: int, nome: Union[str, None] = None):
    return {"item_id": item_id, "nome": nome}