# models/event.py

from dataclasses import dataclass

from models.board import Board


@dataclass
class Event:
    id: int
    name: str
    date: str
    partner_id: str
    location: str = ""
    notes: str = ""
    boards: list[Board] = None
