from database import get_connection


class PartnerRepository:
    @staticmethod
    def create(name: str, ebu_number: str):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO partners (name, ebu_number)
            VALUES (?, ?)
        """,
            (name, ebu_number),
        )

        conn.commit()
        partner_id = cur.lastrowid
        conn.close()

        return partner_id

    @staticmethod
    def get_by_id(partner_id: int):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT id, name, ebu_number
            FROM partners
            WHERE id = ?
        """,
            (partner_id,),
        )

        row = cur.fetchone()
        conn.close()

        return row

    @staticmethod
    def get_all():
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, name, ebu_number
            FROM partners
            ORDER BY name ASC
        """)

        rows = cur.fetchall()
        conn.close()

        return rows

    # UPDATE
    @staticmethod
    def update(partner_id: int, name: str, ebu_number: str):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE partners
            SET name = ?, ebu_number = ?
            WHERE id = ?
        """,
            (name, ebu_number, partner_id),
        )

        conn.commit()
        conn.close()

    # DELETE (optional, see note below)
    @staticmethod
    def delete(partner_id: int):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            DELETE FROM partners
            WHERE id = ?
        """,
            (partner_id,),
        )

        conn.commit()
        conn.close()
