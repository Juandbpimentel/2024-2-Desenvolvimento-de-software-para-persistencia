from typing import List
from pydantic import BaseModel
import logging
import yaml
import json


class Pessoa(BaseModel):
    id: int|None
    name: str|None
    age: int|None


pessoasDesserializadas: List[Pessoa] = []


def carregarYaml(nomeDoArquivo: str):
    print('Carregando dados de configuração')
    with open(nomeDoArquivo, "r") as file:
        dadosCarregados = yaml.safe_load(file)
        print('Dados de configuração carregados')
        return dadosCarregados


def configurarLog(configuracao):
    print('Configurando log')
    logging.basicConfig(
        level=configuracao["level"],
        filename=configuracao["file"],
        format=configuracao["format"],
    )
    print('Log configurado com sucesso!')
    logging.info('____________________________________ Log iniciado ____________________________________')


def carregarJson(nomeDoArquivo: str):
    print(f'Carregando dados do arquivo JSON \'{nomeDoArquivo}\'')
    logging.info('Iniciando leitura do arquivo JSON \'{nomeDoArquivo}\'')
    pessoas: List[Pessoa] = []
    with open(nomeDoArquivo, "r", encoding="utf-8") as file:
        dadosCarregados = json.load(file)
        for dadosDePessoa in dadosCarregados["pessoas"]:
            novaPessoa = Pessoa(
                id=dadosDePessoa["id"],
                name=dadosDePessoa["name"],
                age=dadosDePessoa["age"],
            )
            pessoas.append(novaPessoa)
        print('Dados carregados com sucesso')
        logging.info(f'Arquivo JSON \'{nomeDoArquivo}\' carregado com sucesso.')
        return pessoas

def processaPessoas(pessoas: List[Pessoa]):
    print('Fazendo processamento das pessoas')
    logging.info('Iniciando processamento das pessoas')
    for pessoa in pessoas:
        if (
                pessoa.id is None
                or pessoa.name is None
                or pessoa.age is None
            ):
            print(f'Pessoa com erro nos dados: {pessoa}')
            logging.warning(f'Erro no registro: Dado inválido: {pessoa}')
            continue
        print(f'Pessoa {pessoa.id}: {pessoa}')
        logging.info(f'Processando registro: {pessoa}')


def configurarLeitor():
    dadosDeConfiguracao = carregarYaml("config.yaml")
    configurarLog(dadosDeConfiguracao["logging"])
    pessoasDesserializadas = carregarJson(dadosDeConfiguracao["data"]["file"])
    processaPessoas(pessoasDesserializadas)
print('Iniciando sistema de leitura e processamento de pessoas')
configurarLeitor()
print('Processamento finalizado! Verifique o log para consulta das operações e erros')