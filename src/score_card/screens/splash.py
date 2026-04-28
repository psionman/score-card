# splash.py
from pathlib import Path

from constants import KV_DIR
from kivy.app import App
from kivy.lang import Builder
from kivy.resources import resource_add_path
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock

resource_add_path(Path(Path(__file__).parent.parent, "images"))
Builder.load_file(str(Path(KV_DIR, "splash.kv")))
from constants import DEBUG_SCREEN


class Splash(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self):
        if not DEBUG_SCREEN:
            Clock.schedule_once(self.go_home, 2.0)  # delay for splash
        ...

    def go_home(self, dt):
        self.manager.current = "event_list"
