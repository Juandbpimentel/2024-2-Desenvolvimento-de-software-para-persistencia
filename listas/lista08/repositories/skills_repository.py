from psycopg2 import sql
from typing import List, Optional
from models import Skill
from database import get_connection

def create_skill(skill: Skill) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO skill (nome, descricao, nivel_necessario, dano_base_da_skill, cura_base_da_skill, custo_de_mana_base, custo_de_vida_base, classe_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        """,
        (skill.nome, skill.descricao, skill.nivel_necessario, skill.dano_base_da_skill, skill.cura_base_da_skill, skill.custo_de_mana_base, skill.custo_de_vida_base, skill.classe_id)
    )
    skill_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return skill_id

def get_skill(skill_id: int) -> Optional[Skill]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM skill WHERE id = %s", (skill_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Skill(
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
    return None

def update_skill(skill_id: int, update_data: dict) -> bool:
    if not update_data:
        return False

    set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
    values = list(update_data.values())
    values.append(skill_id)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        sql.SQL(f"UPDATE skill SET {set_clause} WHERE id = %s"),
        values
    )
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return updated

def delete_skill(skill_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM skill WHERE id = %s", (skill_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def get_all_skills() -> List[Skill]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM skill")
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