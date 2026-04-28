# models/partner/py

from dataclasses import dataclass


@dataclass
class Partner:
    id: int
    name: str
    ebu_number: str
