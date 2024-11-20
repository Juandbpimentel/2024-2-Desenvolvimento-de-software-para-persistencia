from typing import Union, List
from http import HTTPStatus
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import csv
import os


app = FastAPI()
CSV_FILE = "database.csv"

#Modelo de dados para o produto
class Produto(BaseModel):
    id: int
    nome: str
    preco: float
    quantidade: int
    is_oferta: Union[bool, None] = None

def lerDadosCsv():
    produtos:List[Produto] = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                produtos.append(Produto(**row))
    return produtos

def escreverDadosCsv(produtos:List[Produto]):
    with open(CSV_FILE, mode="w", newline="") as file:
        fieldnames = ['id','nome','preco','quantidade','is_oferta']
        writer = csv.DictWriter(file,fieldnames=fieldnames)
        writer.writeheader()
        for produto in produtos:
            writer.writerow(produto.dict())


@app.get("/hi", status_code=HTTPStatus.OK)
async def helloWorld():
    return {"msg": "Hello World!"}


@app.get("/produtos/{produto_id}", status_code=HTTPStatus.OK, response_model=Produto)
def lerProduto(produto_id: int):
    produtos = lerDadosCsv()
    for produto_atual in produtos:
        if produto_atual.id == produto_id:
            return produto_atual
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND,detail='Produto não encontrado')

@app.get("/produtos/", response_model=List[Produto])
def listarProdutos():
    return lerDadosCsv()

@app.post("/produtos/",response_model=Produto, status_code=HTTPStatus.CREATED)
def adicionarProduto(produto: Produto):
    produtos = lerDadosCsv()
    if any(produto.id == produto_atual.id for produto_atual in produtos):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Já existe um produto com esse ID no sistema.")
    produtos.append(produto)
    escreverDadosCsv(produtos)
    return produto

@app.put("/produtos/{produto_id}", response_model=Produto, status_code=HTTPStatus.OK)
def atualizarProduto(produto_id: int,produto_atualizado: Produto):
    produtos = lerDadosCsv()
    for indice,produto_atual in enumerate(produtos):
        if produto_id == produto_atual.id:
            if produto_atualizado.id != produto_id:
                produto_atualizado.id = produto_id
            produtos[indice] = produto_atualizado
            escreverDadosCsv(produtos)
            return produto_atualizado        
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Não existe um item com esse ID no sistema.")

@app.delete("/produtos/{produto_id}", status_code=HTTPStatus.OK)
def removerProduto(produto_id: int):
    produtos = lerDadosCsv()
    for indice,produtoAtual in enumerate(produtos):
        if produtoAtual.id == produto_id:
            produto = produtos.pop(indice)
            escreverDadosCsv(produtos)
            return {"msg":"Produto deletado com sucesso!","produto":produto}
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Não existe um produto com esse ID no sistema.")