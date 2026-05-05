from pathlib import Path
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder

from constants import KV_DIR

Builder.load_file(str(Path(KV_DIR, "theme.kv")))
Builder.load_file(str(Path(KV_DIR, "not_implemented.kv")))


class NotImplementedForm(MDScreen): ...
