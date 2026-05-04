# repositories/settings.py

from database import get_connection


class SettingsRepository:
    @staticmethod
    def create(email_address: str):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO settings (email_address)
            VALUES (?)
        """,
            (email_address,),
        )

        conn.commit()
        settings_id = 1
        conn.close()

        return settings_id

    @staticmethod
    def get_by_id(settings_id: int):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT id, email_address
            FROM settings
            WHERE id = ?
        """,
            (1,),
        )

        row = cur.fetchone()
        conn.close()

        return row

    @staticmethod
    def get_all():
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, email_address
            FROM settings
            ORDER BY name ASC
        """)

        rows = cur.fetchall()
        conn.close()

        return rows

    # UPDATE
    @staticmethod
    def update(email_address: str):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE settings
            SET email_address = ?
            WHERE id = ?
        """,
            (email_address, 1),
        )

        conn.commit()
        conn.close()

    # DELETE (optional, see note below)
    @staticmethod
    def delete():
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            DELETE FROM settings
            WHERE id = ?
        """,
            (1,),
        )

        conn.commit()
        conn.close()
