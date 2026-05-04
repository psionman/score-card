# models/settings.py

from dataclasses import dataclass


@dataclass
class Settings:
    id: int
    email_address: str
