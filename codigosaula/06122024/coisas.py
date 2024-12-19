import psycopg2 as pg
import sys

#Criando o banco
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT # <-- ADD THIS LINE

con = pg.connect(dbname='postgres',
      user='postgres', host='localhost',
      password='pgpass')

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE

cur = con.cursor()

# Use the psycopg2.sql module instead of string concatenation 
# in order to avoid sql injection attacks.
try:
	cur.execute('''CREATE DATABASE persistencia''')
except Exception as error:
    if not isinstance(error,pg.errors.DuplicateDatabase):
    	sys.exit("Erro ao criar banco de dados")


# Conectando no banco
con = pg.connect(
        dbname='persistencia',
        user='postgres',
        password='pgpass',
        host='localhost',
        port='5432'
	)

cursor = con.cursor()

try:
	cursor.execute('''
            CREATE TABLE IF NOT EXISTS alunos (
                id SERIAL PRIMARY KEY,
                nome TEXT NOT NULL
            )
	''')
	cursor.execute('INSERT INTO alunos (nome) VALUES (%s)', ('Maria',))
	cursor.execute('INSERT INTO alunos (nome) VALUES (%s)', ('João',))
	con.commit()
	print('deu certo')
except Exception as e:
	conn.rollback()	
	print(f'Erro ao executar operações no banco de dados: {e}')