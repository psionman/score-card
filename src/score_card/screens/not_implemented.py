from pathlib import Path

from constants import KV_DIR
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen

Builder.load_file(str(Path(KV_DIR, "theme.kv")))
Builder.load_file(str(Path(KV_DIR, "not_implemented.kv")))


class NotImplementedForm(MDScreen): ...
