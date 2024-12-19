import psycopg2 as pg

# Conectando no banco
con = pg.connect(
    host="localhost", dbname="projeto", user="postgres", postgrespassword="pgpass"
)
cursor = con.cursor()

try:
    cursor.execute(
        '''
        Create table if not exists usuario(
            id serial primary key,
            nome text not null
        )
        '''
        
    )
except Exception as e:
    print(f"Erro: {e}")