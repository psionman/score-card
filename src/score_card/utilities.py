# utilities.py
import logging
import traceback
from kivy.uix.popup import Popup
from kivy.uix.label import Label

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
