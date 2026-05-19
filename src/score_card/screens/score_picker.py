# screens/score_picker.py

from pathlib import Path

from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

from constants import KV_DIR

HIGHLIGHT_DELAY = 0.67

_kv_loaded = False


def _load_kv():
    global _kv_loaded
    if not _kv_loaded:
        Builder.load_file(str(Path(KV_DIR, "score_picker.kv")))
        _kv_loaded = True


_load_kv()


class ScorePicker(BoxLayout):
    """
    Phone-friendly score picker for Bridge.
    """

    score = StringProperty("")
    parent_screen = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._score = ""

    def set_score(self, score: str) -> None:
        if score == 0:
            score = ""
        self._score = str(score)
        self.ids.score.text = self._score

    # ==================================================================
    # Selection handlers (called from .kv)
    # ==================================================================
    def add_score_digit(self, score_digit: str):
        self._score += score_digit
        self.ids.score.text = self._score
        self._highlight(self.ids.level_grid, score_digit)

    def backspace(self):
        if not self._score:
            return
        self._score = self._score[:-1]
        self.ids.score.text = self._score

    # ==================================================================
    # Highlight selected button
    # ==================================================================
    def _highlight(self, grid, selected_text: str):
        for btn in grid.children:
            btn.selected = btn.text == selected_text

        if hasattr(self, "_highlight_event"):
            self._highlight_event.cancel()

        self._highlight_event = Clock.schedule_once(
            lambda dt: self._clear_highlight(grid), HIGHLIGHT_DELAY
        )

    def _clear_highlight(self, grid):
        for btn in grid.children:
            btn.selected = False

    def reset(self):
        """Call this every time the picker is shown for a new selection."""
        self._score = ""
        self._update_display()

        for grid in (self.ids.level_grid, self.ids.suit_grid):
            for btn in grid.children:
                btn.selected = False

    def cancel(self):
        self.parent_screen._score_modal.dismiss()

    def confirm(self):
        if not self._score:
            return
        print("C", self._score)
        self.parent_screen.update_score(self._score)
        self.parent_screen._score_modal.dismiss()
