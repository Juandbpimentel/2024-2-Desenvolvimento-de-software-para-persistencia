from psycopg2 import sql
from typing import List, Optional
from models import Classe
from database import get_connection
from models import Personagem
from models import Skill
from repositories import personagem_repository


def create_classe(classe: Classe) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO classe (nome, descricao, escala_dano_por_nivel, escala_vida_por_nivel, escala_mana_por_nivel)
        VALUES (%s, %s, %s, %s, %s) RETURNING id
        """,
        (classe.nome, classe.descricao, classe.escala_dano_por_nivel, classe.escala_vida_por_nivel, classe.escala_mana_por_nivel)
    )
    classe_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return classe_id

def get_classe(classe_id: int) -> Optional[Classe]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM classe WHERE id = %s", (classe_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Classe(
            id=row[0],
            nome=row[1],
            descricao=row[2],
            escala_dano_por_nivel=row[3],
            escala_vida_por_nivel=row[4],
            escala_mana_por_nivel=row[5]
        )
    return None

def update_classe(classe_id: int, update_data: dict) -> bool:
    if not update_data:
        return False

    set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
    values = list(update_data.values())
    values.append(classe_id)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        sql.SQL(f"UPDATE classe SET {set_clause} WHERE id = %s"),
        values
    )
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return updated

def delete_classe(classe_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM classe WHERE id = %s", (classe_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def get_all_classes() -> List[Classe]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM classe")
    rows = cursor.fetchall()
    conn.close()
    return [
        Classe(
            id=row[0],
            nome=row[1],
            descricao=row[2],
            escala_dano_por_nivel=row[3],
            escala_vida_por_nivel=row[4],
            escala_mana_por_nivel=row[5]
        )
        for row in rows
    ]

def get_skills(classe_id: int) -> List[Skill]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM skill WHERE classe_id = %s", (classe_id,))
    rows = cursor.fetchall()
    conn.close()
    return [
        Skill(
            id=row[0],
            nome=row[1],
            descricao=row[2],
            nivel_necessario=row[3],
            dano_base_da_skill=row[4],
            cura_base_da_skill=row[5],
            custo_de_mana_base=row[6],
            custo_de_vida_base=row[7],
            classe_id=row[8]
        )
        for row in rows
    ]

def get_personagens_with_classe(classe_id: int) -> List[Personagem]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personagem WHERE classe_id = %s", (classe_id,))
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return []
    return [
        personagem_repository.get_personagem(row[0])
        for row in rows
    ]