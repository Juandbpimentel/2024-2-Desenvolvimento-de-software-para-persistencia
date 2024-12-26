from psycopg2 import sql
from typing import List, Optional
from models import Guilda
from database import get_connection
from models import Personagem
from repositories import personagem_repository


def create_guilda(guilda: Guilda) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO guilda (nome, descricao, dono_id)
        VALUES (%s, %s, %s) RETURNING id
        """,
        (guilda.nome, guilda.descricao, guilda.dono_id)
    )
    guilda_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return guilda_id


def get_guilda(guilda_id: int) -> Optional[Guilda]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM guilda WHERE id = %s", (guilda_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Guilda(
            id=row[0],
            nome=row[1],
            descricao=row[2],
            dono_id=row[3],
            dono=get_dono_guilda(row[0]),
            personagens=get_personagens_guilda(row[0])
        )
    return None


def update_guilda(guilda_id: int, update_data: dict) -> bool:
    if not update_data:
        return False

    set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
    values = list(update_data.values())
    values.append(guilda_id)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        sql.SQL(f"UPDATE guilda SET {set_clause} WHERE id = %s"),
        values
    )
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return updated


def delete_guilda(guilda_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM guilda WHERE id = %s", (guilda_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


def get_all_guildas() -> List[Guilda]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM guilda")
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return []
    return [
        Guilda(
            id=row[0],
            nome=row[1],
            descricao=row[2],
            dono_id=row[3]
        )
        for row in rows
    ]


def get_dono_guilda(guilda_id: int) -> Optional[Personagem]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT p from personagem p inner join guilda g on p.id = g.dono_id where g.id = %s", (guilda_id,))
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
            classe_id=row[12],
            guilda_id=row[13],
            guilda=get_guilda(row[13]),
            classe=personagem_repository.get_classe(row[0]),
            skills=personagem_repository.get_skills(row[0])

        )


def get_personagens_guilda(guilda_id: int) -> List[Personagem]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personagem WHERE guilda_id = %s", (guilda_id,))
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
            guilda=get_guilda(row[13]),
            classe=personagem_repository.get_classe(row[0]),
            skills=personagem_repository.get_skills(row[0])
        )
        for row in rows
    ]


def get_guilda_total_power(guilda_id: int) -> float:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT sum(poder) from personagem where guilda_id = %s", (guilda_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0] or 0


def get_guilda_count_participants(guilda_id: int) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT count(id) from personagem where guilda_id = %s", (guilda_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0] or 0


def get_most_powerful_personagem_guilda(guilda_id: int) -> Optional[Personagem]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT max(poder) from personagem where guilda_id = %s", (guilda_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0] or 0


def get_most_powerful_guilda() -> Optional[Guilda]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT guilda_com_poder.id, guilda_com_poder.nome, guilda_com_poder.descricao, guilda_com_poder.dono_id, MAX(total_power) as max_power
        FROM (
            SELECT g.id, g.nome, g.descricao, g.dono_id, SUM(p.poder) as total_power
            FROM guilda g
            INNER JOIN personagem p ON g.id = p.guilda_id
            GROUP BY g.id
            ORDER BY total_power DESC
        ) as guilda_com_poder
        GROUP BY guilda_com_poder.id, guilda_com_poder.nome, guilda_com_poder.descricao, guilda_com_poder.dono_id
        ORDER BY max_power DESC
        LIMIT 1
        """
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0] or 0

def get_least_powerful_guilda() -> Optional[Guilda]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT guilda_com_poder.id, guilda_com_poder.nome, guilda_com_poder.descricao, guilda_com_poder.dono_id, MIN(total_power) as min_power
        FROM (
            SELECT g.id, g.nome, g.descricao, g.dono_id, SUM(p.poder) as total_power
            FROM guilda g
            INNER JOIN personagem p ON g.id = p.guilda_id
            GROUP BY g.id
        ) as guilda_com_poder
        GROUP BY guilda_com_poder.id, guilda_com_poder.nome, guilda_com_poder.descricao, guilda_com_poder.dono_id
        LIMIT 1
        """
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0] or 0
