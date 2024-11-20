from typing import List
import xml.etree.ElementTree as ET
from http import HTTPStatus
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os


app = FastAPI()
XML_FILE = "livros.xml"


# Modelo de dados para o livro
class Livro(BaseModel):
    id: int
    titulo: str
    autor: str
    ano: int
    genero: str


def lerDadosXML():
    livros: List[Livro] = []
    if os.path.exists(XML_FILE):
        tree = ET.parse(XML_FILE)
        root = tree.getroot()
        for elem in root.findall("livro"):
            livro = Livro(
                id=int(elem.find("id").text),
                titulo=elem.find("titulo").text,
                autor=elem.find("autor").text,
                ano=int(elem.find("ano").text),
                genero=elem.find("genero").text,
            )
            livros.append(livro)
    return livros


def escreverDadosXML(livros: List[Livro]):
    root = ET.Element("livros")
    for livro in livros:
        livro_elem = ET.SubElement(root, "livro")
        ET.SubElement(livro_elem, "id").text = str(livro.id)
        ET.SubElement(livro_elem, "titulo").text = livro.titulo
        ET.SubElement(livro_elem, "autor").text = livro.autor
        ET.SubElement(livro_elem, "ano").text = str(livro.ano)
        ET.SubElement(livro_elem, "genero").text = livro.genero
        tree = ET.ElementTree(root)
        tree.write(XML_FILE)


@app.get("/", status_code=HTTPStatus.OK)
async def helloWorld():
    return {"msg": "Hello World!"}


@app.post(
    "/livros/",
    response_model=Livro,
    status_code=HTTPStatus.CREATED,
    description="Recebe um json para inserer um livro no xml",
    summary="Criar livro",
)
def criarLivro(livro: Livro):
    livros = lerDadosXML()
    if any(livro.id == livro_atual.id for livro_atual in livros):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Já existe um livro com esse ID no sistema.",
        )
    livros.append(livro)
    escreverDadosXML(livros)
    return livro


@app.get(
    "/livros/",
    response_model=List[Livro],
    description="Listar todos os livros do xml",
    summary="Listar livros",
)
def listarLivros():
    return lerDadosXML()


@app.get(
    "/livros/{livro_id}",
    status_code=HTTPStatus.OK,
    response_model=Livro,
    description="Utilizar o id do livro para resgatar ele do xml",
    summary="Ler livro",
)
def lerLivro(livro_id: int):
    livros = lerDadosXML()
    for livro_atual in livros:
        if livro_atual.id == livro_id:
            return livro_atual
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Livro não encontrado")


@app.put(
    "/livros/{livro_id}",
    response_model=Livro,
    status_code=HTTPStatus.OK,
    description="Utilizar o id do livro e um livro no body para atualizar um livro do xml",
    summary="Atualizar livro",
)
def atualizarLivro(livro_id: int, livro_atualizado: Livro):
    livros = lerDadosXML()
    for indice, livro_atual in enumerate(livros):
        if livro_id == livro_atual.id:
            if livro_atualizado.id != livro_id:
                livro_atualizado.id = livro_id
            livros[indice] = livro_atualizado
            escreverDadosXML(livros)
            return livro_atualizado
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail="Não existe um item com esse ID no sistema.",
    )


@app.delete(
    "/livros/{livro_id}",
    status_code=HTTPStatus.OK,
    description="Utilizar o id do livro para remover ele do xml",
    summary="Remover livro",
)
def removerLivro(livro_id: int):
    livros = lerDadosXML()
    for indice, livroAtual in enumerate(livros):
        if livroAtual.id == livro_id:
            livro = livros.pop(indice)
            escreverDadosXML(livros)
            return {"msg": "Livro deletado com sucesso!", "livro": livro}
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail="Não existe um livro com esse ID no sistema.",
    )
