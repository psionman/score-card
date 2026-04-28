# services/board.py

from models.board import Board
from repositories.board import BoardRepository


class BoardService:
    @staticmethod
    def create_board(
        event_id: int,
        board_number: int,
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
        return BoardRepository.create(
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
        )

    @staticmethod
    def get_boards_for_event(event_id: int):
        rows = BoardRepository.get_by_event(event_id)

        boards = []

        for r in rows:
            boards.append(
                Board(
                    id=r[0],
                    event_id=r[1],
                    board_number=r[2],
                    vulnerable=r[3],
                    orientation=r[4],
                    opponents=r[5],
                    contract=r[6],
                    declarer=r[7],
                    lead=r[8],
                    tricks=r[9],
                    score=r[10],
                    section=r[11],
                    team_score=r[12],
                    imps=r[13],
                    notes=r[14],
                )
            )

        return boards

    @staticmethod
    def update_board(board_id: int, **kwargs):
        BoardRepository.update(board_id, **kwargs)
