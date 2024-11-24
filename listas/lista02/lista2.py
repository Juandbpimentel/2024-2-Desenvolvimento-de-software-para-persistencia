import zipfile
import os

def verificaLetrasEPalavras(texto:str) -> dict[str,str,str]:
    qtdCaracteres = len(texto)
    qtdDeCaracteresSemEspacoEEnter = 0
    for i in range(qtdCaracteres):
        if texto[i] != "\n":
            qtdDeCaracteresSemEspacoEEnter += 1
            
    texto = list(filter(lambda x: x != "", texto.replace("\n", " ").split(" ")))
    qtdPalavras = len(texto)
    return {"qtdCaracteres":qtdDeCaracteresSemEspacoEEnter, "qtdPalavras":qtdPalavras}

def retornaDadosDeArquivo(arquivoUrl:str) -> dict[str,str,str]:
    with open(arquivoUrl, "r",encoding='utf-8') as arquivo:
        texto = str(arquivo.read())
        return verificaLetrasEPalavras(texto)
    
def processarDados(pastaTextos:str, arquivoFinal:str) -> None:
    with open (arquivoFinal,'w',encoding='utf-8') as arquivoFinal:
        try:
            if not os.path.exists(pastaTextos):
                raise Exception("Pasta não encontrada")
            if not os.path.isdir(pastaTextos):
                raise Exception("Caminho não é uma pasta")
            if not os.listdir(pastaTextos):
                raise Exception("Pasta vazia")
            countArquivosTxt = 0
            for nomeArquivo in os.listdir(pastaTextos):
                if nomeArquivo.endswith('.txt'):
                    countArquivosTxt += 1
                    caminhoArquivo = os.path.join(pastaTextos,nomeArquivo)
                    dadoDoArquivoDeTexto = retornaDadosDeArquivo(caminhoArquivo)
                    arquivoFinal.write(f"{nomeArquivo}: {dadoDoArquivoDeTexto['qtdPalavras']} palavras, {dadoDoArquivoDeTexto['qtdCaracteres']} caracteres\n")
            if countArquivosTxt == 0:
                raise Exception("Nenhum arquivo .txt encontrado")
        except Exception as e:
            print(f"Erro: {e}")
            raise(e)
            
def salvarEmZip(arquivoFinal:str,arquivoZip:str) -> None:
    with zipfile.ZipFile(arquivoZip, 'w', zipfile.ZIP_STORED) as zipDoArquivo:
        zipDoArquivo.write(arquivoFinal)
        
def listarArquivosZip(arquivoZip:str) -> None:
    with zipfile.ZipFile(arquivoZip, 'r') as zipDoArquivo:
        print("Arquivos no ZIP:")
        for arquivo in zipDoArquivo.namelist():
            print(arquivo)



processarDados("textos","consolidado.txt")
salvarEmZip('consolidado.txt','saida.zip')
listarArquivosZip('saida.zip')
