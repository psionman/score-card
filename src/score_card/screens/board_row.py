from pathlib import Path

from constants import KV_DIR
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout

Builder.load_file(str(Path(KV_DIR, "board_row.kv")))

# def _load_kv():
#     global _kv_loaded
#     if not _kv_loaded:
#         Builder.load_file(str(Path(KV_DIR, "board_row.kv")))
#         _kv_loaded = True


# _load_kv()


class BoardRow(MDBoxLayout):
    board = StringProperty()
    score = StringProperty()
    team_score = StringProperty()
    imps = StringProperty()
