# app.py

import os
from pathlib import Path

# Must be before any kivy imports when testing on desktop
from kivy.config import Config

if os.environ.get("KIVY_BUILD") != "android":
    Config.set("graphics", "width", "360")
    Config.set("graphics", "height", "780")
    Config.set("graphics", "dpi", "160")
    Config.set("graphics", "resizable", "0")

from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivymd.app import MDApp
from kivy.core.text import LabelBase

from database import init_db
from constants import BASE_DIR, DEBUG_SCREEN, INITIALISE_DB
from navigation import NavigationService
from screens.splash import Splash

from screens.partner_form import PartnerFormScreen
from screens.partner_list import PartnerListScreen

from screens.event_form import EventForm
from screens.event_list import EventList

from screens.board_form import BoardForm
from screens.board_list import BoardList
from screens.contract_picker import ContractPicker

from screens.not_implemented import NotImplementedForm


LabelBase.register(
    "DejaVuSans",
    fn_regular=str(Path(BASE_DIR, "fonts", "DejaVuSans.ttf"))
)

class ScoreCard(MDApp):
    title = "Score card"
    icon = "src/score_card/images/score_card_icon.png"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_event = None

    def set_event(self, event):
        self.current_event = event

    def get_event(self):
        return self.current_event

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"

        if INITIALISE_DB:
            init_db()

        self.sm = ScreenManager(transition=FadeTransition(duration=0.3))

        self.nav = NavigationService(self.sm)

        self.sm .add_widget(Splash(name="splash"))

        self.sm.add_widget(PartnerFormScreen(name="partner_form"))
        self.sm.add_widget(PartnerListScreen(name="partner_list"))

        self.sm.add_widget(EventForm(name="event_form"))
        self.sm.add_widget(EventList(name="event_list"))

        self.sm.add_widget(BoardForm(name="board_form"))
        self.sm.add_widget(BoardList(name="board_list"))

        self.sm.add_widget(NotImplementedForm(name="not_implemented_form"))

        self.sm.current = DEBUG_SCREEN or "splash"

        return self.sm
