# repositories/board.py

from database import get_connection


class BoardRepository:
    @staticmethod
    def create(
        event_id,
        board_number,
        vulnerable,
        orientation,
        opponents,
        contract,
        declarer,
        lead,
        tricks,
        score,
        section,
        team_score,
        imps,
        notes,
    ):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO boards (
                event_id,
                board_number,
                vulnerable,
                orientation,
                opponents,
                contract,
                declarer,
                lead,
                tricks,
                score,
                section,
                team_score,
                imps,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                event_id,
                board_number,
                vulnerable,
                orientation,
                opponents,
                contract,
                declarer,
                lead,
                tricks,
                score,
                section,
                team_score,
                imps,
                notes
            ),
        )

        conn.commit()
        board_id = cur.lastrowid
        conn.close()

        return board_id

    @staticmethod
    def get_by_event(event_id: int):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT
                id,
                event_id,
                board_number,
                vulnerable,
                orientation,
                opponents,
                contract,
                declarer,
                lead,
                tricks,
                score,
                section,
                team_score,
                imps,
                notes
            FROM boards
            WHERE event_id = ?
            ORDER BY board_number ASC
        """,
            (event_id,),
        )

        rows = cur.fetchall()
        conn.close()

        return rows

    @staticmethod
    def update(
        board_id,
        board_number,
        vulnerable,
        orientation,
        opponents,
        contract,
        declarer,
        lead,
        tricks,
        score,
        section,
        team_score,
        imps,
        notes,
    ):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE boards SET
                board_number = ?,
                vulnerable = ?,
                orientation = ?,
                opponents = ?,
                contract = ?,
                declarer = ?,
                lead = ?,
                tricks = ?,
                score = ?,
                section = ?,
                team_score = ?,
                imps = ?,
                notes = ?
            WHERE id = ?
            """,
            (
                board_number,
                vulnerable,
                orientation,
                opponents,
                contract,
                declarer,
                lead,
                tricks,
                score,
                section,
                team_score,
                imps,
                notes,
                board_id,
            ),
        )

        conn.commit()
        conn.close()
