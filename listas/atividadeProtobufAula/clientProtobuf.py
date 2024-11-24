import pessoa_pb2
import socket

# Conectar ao servidor
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5000))

# Receber os dados
data = client.recv(1024)

# Desserializar os dados
pessoa = pessoa_pb2.Person()
pessoa.ParseFromString(data)

# Verificar os campos
print(f"Recebido: {pessoa.name}, {pessoa.id}, {pessoa.email}")  # Isso deve funcionar
client.close()
