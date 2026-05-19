from kivy.event import EventDispatcher
from kivy.properties import (
    NumericProperty,
    StringProperty,
    ObjectProperty,
)
from typing import Optional


class Board(EventDispatcher):
    id = NumericProperty(0)
    event_id = NumericProperty(0)

    board_number = NumericProperty(0)

    vulnerable = StringProperty("")
    orientation = StringProperty("NS")

    opponents = NumericProperty(0)

    contract = StringProperty("")
    declarer = StringProperty("")
    lead = StringProperty("")

    tricks = NumericProperty(0)

    score = NumericProperty(0)

    section = StringProperty("")
    team_score = NumericProperty(0)
    imps = NumericProperty(0)

    notes = StringProperty("")
