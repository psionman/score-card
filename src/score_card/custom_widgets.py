# custom_widgets.py

from pathlib import Path
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, ColorProperty
from kivy.metrics import dp
from kivymd.app import MDApp
from kivy.graphics import Color, RoundedRectangle
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.widget import Widget

from constants import KV_DIR

class Divider(Widget):
    pass

Factory.register('Divider', cls=Divider)

class SuitButton(Button):
    selected = BooleanProperty(False)
    suit_color = ColorProperty((0, 0, 0, 1))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0.9, 0.9, 0.9, 0)
        self.bind(
            selected=self._redraw,
            pos=self._redraw,
            size=self._redraw,
            suit_color=self._redraw)

    def _redraw(self, *args):
        app = MDApp.get_running_app()
        if app is None:
            return
        self.canvas.before.clear()
        with self.canvas.before:
            if self.selected:
                Color(*app.theme_cls.primary_color)
            else:
                Color(1, 1, 1, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(4)])
        self.color = (1, 1, 1, 1) if self.selected else self.suit_color

Builder.load_file(str(Path(KV_DIR, "custom_widgets.kv")))
