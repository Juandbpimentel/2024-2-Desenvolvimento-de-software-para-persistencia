from psycopg2 import sql
from typing import List, Optional, Type

from models import Classe
from models import Guilda
from models import Personagem
from database import get_connection
from models import Skill


def create_personagem(personagem: Personagem) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO personagem (nome, nivel, poder, xp_atual, xp_proximo_nivel, hp_atual, hp_max, mana_atual, mana_max, forca, defesa, classe_id, guilda_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        """,
        (personagem.nome, personagem.nivel, personagem.xp_atual, personagem.xp_proximo_nivel, personagem.hp_atual,
         personagem.hp_max, personagem.mana_atual, personagem.mana_max, personagem.forca, personagem.defesa,
         personagem.classe_id, personagem.guilda_id)
    )
    personagem_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return personagem_id


def get_personagem(personagem_id: int) -> Optional[Personagem]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personagem WHERE id = %s", (personagem_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Personagem(
            id=row[0],
            nome=row[1],
            nivel=row[2],
            poder=row[3],
            xp_atual=row[4],
            xp_proximo_nivel=row[5],
            hp_atual=row[6],
            hp_max=row[7],
            mana_atual=row[8],
            mana_max=row[9],
            forca=row[10],
            defesa=row[11],
            classe_id=row[11],
            guilda_id=row[13],
            skills=get_skills(row[0])
        )
    return None


def update_personagem(personagem_id: int, update_data: dict) -> bool:
    if not update_data:
        return False

    set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
    values = list(update_data.values())
    values.append(personagem_id)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        sql.SQL(f"UPDATE personagem SET {set_clause} WHERE id = %s"),
        values
    )
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return updated


def delete_personagem(personagem_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM personagem WHERE id = %s", (personagem_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


def get_all_personagens() -> List[Personagem]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personagem")
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return []
    return [
        Personagem(
            id=row[0],
            nome=row[1],
            nivel=row[2],
            poder=row[3],
            xp_atual=row[4],
            xp_proximo_nivel=row[5],
            hp_atual=row[6],
            hp_max=row[7],
            mana_atual=row[8],
            mana_max=row[9],
            forca=row[10],
            defesa=row[11],
            classe_id=row[12],
            guilda_id=row[13],
            skills=get_skills(row[0])
        )
        for row in rows
    ]


def get_guilda(personagem_id: int) -> Optional[Guilda]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM guilda "
                   "INNER JOIN personagem ON guilda.id = personagem.guilda_id "
                   "WHERE personagem.id = %s", (personagem_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Guilda(
            id=row[0],
            nome=row[1],
            descricao=row[2],
            dono_id=row[3]
        )


def get_classe(personagem_id: int) -> Optional[Classe]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM classe INNER JOIN personagem ON classe.id = personagem.classe_id WHERE personagem.id = %s",
        (personagem_id,))
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


# Busca complexa
def get_skills(personagem_id: int) -> List[Skill]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT s FROM skill s
                    INNER JOIN personagem p ON s.classe_id = p.classe_id
                    WHERE p.id = %s AND s.nivel_necessario <= p.nivel
                    """, (personagem_id,))
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return []
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
