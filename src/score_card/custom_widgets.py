# custom_widgets.py

from collections.abc import Callable
from pathlib import Path

from constants import KV_DIR
from kivy.factory import Factory
from kivy.graphics import Color, RoundedRectangle
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import BooleanProperty, ColorProperty, StringProperty
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.list import IconLeftWidget, OneLineIconListItem
from kivymd.uix.menu import MDDropdownMenu


class Divider(Widget):
    pass


Builder.load_string("""
<IconListItem>:
    IconLeftWidget:
        icon: root.icon
""")


class IconListItem(OneLineIconListItem):
    icon = StringProperty()


Factory.register("Divider", cls=Divider)
Factory.register("IconLeftWidget", cls=IconLeftWidget)


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
            suit_color=self._redraw,
        )

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


def _get_menu_divider():
    return {
        "viewclass": "Divider",
        "height": dp(1),
        "on_release": lambda: None,
    }


menu_divider = _get_menu_divider()


def menu_icon_item(text: str, icon: str, handler: Callable) -> dict:
    return {
        "text": text,
        "icon": icon,
        "viewclass": "IconListItem",
        "on_release": lambda x=text: handler(text),
    }


def menu_handler(caller, menu_items: list):
    menu_items = menu_items
    menu = MDDropdownMenu(
        caller=caller,
        items=menu_items,
        width_mult=4,
    )
    menu.open()
    return menu
