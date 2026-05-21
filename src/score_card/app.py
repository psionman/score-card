# app.py

from dataclasses import dataclass
import os
from pathlib import Path
from dataclasses import dataclass

# Must be before any kivy imports when testing on desktop
from kivy.config import Config

if os.environ.get("KIVY_BUILD") != "android":
    Config.set("graphics", "width", "360")
    Config.set("graphics", "height", "780")
    Config.set("graphics", "dpi", "160")
    Config.set("graphics", "resizable", "0")

from constants import BASE_DIR, DEBUG_SCREEN, INITIALISE_DB
from database import init_db
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import FadeTransition, NoTransition, ScreenManager
from kivymd.app import MDApp
from navigation import NavigationService
from screens.board_form import BoardForm
from screens.board_list import BoardList
from screens.event_form import EventForm
from screens.event_list import EventList
from screens.not_implemented import NotImplementedForm
from screens.partner_form import PartnerFormScreen
from screens.partner_list import PartnerListScreen
from screens.section_board_list import SectionBoardList
from screens.section_list import SectionList
from screens.settings_form import SettingsFormScreen
from services.settings import SettingsService

LabelBase.register(
    "DejaVuSans", fn_regular=str(Path(BASE_DIR, "fonts", "DejaVuSans.ttf"))
)


@dataclass
class LastBoard:
    board_number: int = 0
    orientation: str = ""
    opponents: int = 0
    section_id: int = 0


class ScoreCard(MDApp):
    title = "Score card"
    icon = "src/score_card/images/score_card_icon.png"

    SCREENS = [
        ("partner_form", PartnerFormScreen),
        ("partner_list", PartnerListScreen),
        ("event_form", EventForm),
        ("event_list", EventList),
        ("board_form", BoardForm),
        ("board_list", BoardList),
        ("section_list", SectionList),
        ("section_board_list", SectionBoardList),
        ("settings_form", SettingsFormScreen),
        ("not_implemented_form", NotImplementedForm),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_event = None
        self.settings = None
        self.last_board = LastBoard()

    def set_event(self, event):
        self.current_event = event

    def set_last_board(self, last_board: list):
        self.last_board = LastBoard(*last_board)

    def get_event(self):
        return self.current_event

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"

        if INITIALISE_DB:
            init_db()

        self.settings = SettingsService.get_settings(1)

        self.sm = ScreenManager(transition=NoTransition())

        self.nav = NavigationService(self.sm)

        for name, screen_class in self.SCREENS:
            self.sm.add_widget(screen_class(name=name))

        self.sm.current = DEBUG_SCREEN or "event_list"

        self.sm.transition = FadeTransition(duration=0.3)

        return self.sm
