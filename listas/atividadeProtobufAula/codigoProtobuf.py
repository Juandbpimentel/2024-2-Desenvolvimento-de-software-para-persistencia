import pessoa_pb2

pessoa = pessoa_pb2.Person()
pessoa.name = "Gabriel Cabelinho"
pessoa.id = 10
pessoa.email = "ZabrielDoCabelin@gemeio.com"

data = pessoa.SerializeToString()
print(data)

#Desserializar
new_persoua = pessoa_pb2.Person()
new_persoua.ParseFromString(data)
print(new_persoua)