import socket
import pessoa_pb2

def create_pessoa():
    pessoa = pessoa_pb2.Person()
    pessoa.name = "Bob"
    pessoa.id = 5678
    pessoa.email = "bob@example.com"
    return pessoa.SerializeToString()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5000))
server.listen(1)
print("Servidor aguardando conexão...")

conn, addr = server.accept()
print(f"Conexão de {addr}")

data = create_pessoa()
conn.sendall(data)
conn.close()
