# widgets/appheader.py
from pathlib import Path

from constants import KV_DIR
from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty
from kivymd.uix.boxlayout import MDBoxLayout

Builder.load_file(str(Path(KV_DIR, "app_header.kv")))


class AppHeader(MDBoxLayout):
    title = StringProperty("")
    subtitle = StringProperty("")

    left_actions = ListProperty([])
    right_actions = ListProperty([])
