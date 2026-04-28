
from database import get_connection


class EventRepository:
    @staticmethod
    def create(name, date, partner_id, location="", notes=""):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO events (name, date, partner_id, location, notes)
            VALUES (?, ?, ?, ?, ?)
        """,
            (name, date, partner_id, location, notes),
        )

        conn.commit()
        event_id = cur.lastrowid
        conn.close()

        return event_id

    @staticmethod
    def update(event_id, name, date, partner_id, location="", notes=""):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE events
            SET name = ?, date = ?, partner_id = ?, location = ?, notes = ?
            WHERE id = ?
        """, (name, date, partner_id, location, notes, event_id))

        conn.commit()
        conn.close()


    @staticmethod
    def get_by_id(event_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT id, name, date, partner_id, location, notes
            FROM events
            WHERE id = ?
        """,
            (event_id,),
        )

        row = cur.fetchone()
        conn.close()

        return row  # raw tuple

    @staticmethod
    def get_all():
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, name, date, partner_id, location, notes
            FROM events
            ORDER BY id DESC
        """)

        rows = cur.fetchall()
        conn.close()

        return rows
