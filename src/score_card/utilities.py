# utilities.py
import logging
import re
import traceback

from constants import SUIT_LABELS
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog


def safe_execute(func):
    """Decorator for catching and logging errors without crashing"""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f">>> ERROR in {func.__name__}: {e}")
            logging.error(traceback.format_exc())

    return wrapper


def show_message(title: str, msg: str):
    popup = Popup(
        title=title,
        content=Label(text=msg),
        size_hint=(0.8, 0.3),
    )
    popup.open()


def suit_to_symbol(text: str) -> str:
    suit_card_re = r"([1-9JQKA]|10)([SHDC])"
    match = re.search(suit_card_re, text)
    rank = match.group(1)
    suit = match.group(2)
    if suit not in SUIT_LABELS:
        return text

    return f"{rank}{SUIT_LABELS.get(suit, suit)}"


def msg_dialog(title, message):
    dialog = MDDialog(
        title=title,
        text=message,
        buttons=[
            MDFlatButton(
                text="CANCEL",
                # theme_text_color="Custom",
                # text_color=self.theme_cls.primary_color,
                on_release=lambda x: dialog.dismiss(),
            ),
        ],
    )
    dialog.open()
