import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

import logging

load_dotenv(".env")
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

BASE_USER_NAME = os.getenv("BASE_USER_NAME")
BASE_PASSWORD = os.getenv("BASE_PASSWORD")
BASE_HOST = os.getenv("BASE_HOST")
BASE_PORT = os.getenv("BASE_PORT")
BASE_DATABASE_NAME = os.getenv("BASE_DATABASE_NAME")

NEW_DATABASE_NAME = os.getenv("NEW_DATABASE_NAME")
NEW_USER = os.getenv("NEW_USER")
NEW_PASSWORD = os.getenv("NEW_PASSWORD")

def create_db_and_tables():
    # Connect to the default database to check if the new database exists
    default_conn = psycopg2.connect(
        dbname=BASE_DATABASE_NAME,
        user=BASE_USER_NAME,
        password=BASE_PASSWORD,
        host=BASE_HOST,
        port=BASE_PORT,
    )
    default_conn.autocommit = True
    default_cursor = default_conn.cursor()

    # Check if the database exists
    default_cursor.execute(
        sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"),
        [NEW_DATABASE_NAME]
    )
    exists = default_cursor.fetchone()
    if not exists:
        default_cursor.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(NEW_DATABASE_NAME)
        ))

    default_conn.close()

    # Connect to the new database
    conn = psycopg2.connect(
        dbname=NEW_DATABASE_NAME,
        user=BASE_USER_NAME,
        password=BASE_PASSWORD,
        host=BASE_HOST,
        port=BASE_PORT,
    )
    cursor = conn.cursor()

    # Create tables without foreign key constraints
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS classe (
        id SERIAL PRIMARY KEY,
        nome TEXT,
        descricao TEXT,
        escala_dano_por_nivel INTEGER,
        escala_vida_por_nivel INTEGER,
        escala_mana_por_nivel INTEGER
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS personagem (
        id SERIAL PRIMARY KEY,
        nome TEXT,
        nivel INTEGER,
        poder INTEGER,
        xp_atual INTEGER,
        xp_proximo_nivel INTEGER,
        hp_atual INTEGER,
        hp_max INTEGER,
        mana_atual INTEGER,
        mana_max INTEGER,
        forca INTEGER,
        defesa INTEGER,
        classe_id INTEGER,
        guilda_id INTEGER
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS guilda (
        id SERIAL PRIMARY KEY,
        nome TEXT,
        descricao TEXT,
        dono_id INTEGER
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS skill (
        id SERIAL PRIMARY KEY,
        nome TEXT,
        descricao TEXT,
        nivel_necessario INTEGER,
        dano_base_da_skill INTEGER,
        cura_base_da_skill INTEGER,
        custo_de_mana_base INTEGER,
        custo_de_vida_base INTEGER,
        classe_id INTEGER,
        FOREIGN KEY(classe_id) REFERENCES classe(id) ON DELETE CASCADE ON UPDATE CASCADE
    )''')

    # Alter tables to add foreign key constraints if they do not exist
    cursor.execute('''
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1
            FROM information_schema.table_constraints
            WHERE constraint_type = 'FOREIGN KEY'
            AND table_name = 'personagem'
            AND constraint_name = 'fk_classe'
        ) THEN
            ALTER TABLE personagem
            ADD CONSTRAINT fk_classe
            FOREIGN KEY (classe_id)
            REFERENCES classe(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE;
        END IF;
    END $$;
    ''')

    cursor.execute('''
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1
            FROM information_schema.table_constraints
            WHERE constraint_type = 'FOREIGN KEY'
            AND table_name = 'personagem'
            AND constraint_name = 'fk_guilda'
        ) THEN
            ALTER TABLE personagem
            ADD CONSTRAINT fk_guilda
            FOREIGN KEY (guilda_id)
            REFERENCES guilda(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE;
        END IF;
    END $$;
    ''')

    cursor.execute('''
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1
            FROM information_schema.table_constraints
            WHERE constraint_type = 'FOREIGN KEY'
            AND table_name = 'guilda'
            AND constraint_name = 'fk_dono'
        ) THEN
            ALTER TABLE guilda
            ADD CONSTRAINT fk_dono
            FOREIGN KEY (dono_id)
            REFERENCES personagem(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE;
        END IF;
    END $$;
    ''')

    # Check if the user exists before creating it
    cursor.execute(
        sql.SQL("SELECT 1 FROM pg_roles WHERE rolname = %s"),
        [NEW_USER]
    )
    user_exists = cursor.fetchone()
    if not user_exists:
        cursor.execute(f"CREATE USER {NEW_USER} WITH PASSWORD '{NEW_PASSWORD}';")

    cursor.execute(f"GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO {NEW_USER};")
    cursor.execute(f"GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO {NEW_USER};")

    conn.commit()
    conn.close()

def get_connection():
    return psycopg2.connect(
        dbname=NEW_DATABASE_NAME,
        user=BASE_USER_NAME,
        password=BASE_PASSWORD,
        host=BASE_HOST,
        port=BASE_PORT,
    )