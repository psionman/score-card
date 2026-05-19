from pathlib import Path

from constants import KV_DIR
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard

Builder.load_file(str(Path(KV_DIR, "board_row.kv")))


class BoardRow(MDCard):
    board = ObjectProperty()


class BoardHeader(MDBoxLayout):
    pass
