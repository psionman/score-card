# models/board.py

from dataclasses import dataclass
from typing import Optional


@dataclass
class Board:
    id: int
    event_id: int

    board_number: int

    vulnerable: Optional[str]  # None | "NW" | "EW" | "All"
    orientation: str  # "NS" | "EW"

    opponents: int

    contract: str
    declarer: str  # "N" | "S" | "E" | "W"
    lead: str

    tricks: int

    score: int  # can be negative

    section: str
    team_score: int  # can be negative
    imps: int  # can be negative
    notes: Optional[str] = ""
