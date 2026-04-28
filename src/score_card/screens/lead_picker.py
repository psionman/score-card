# screens/lead_picker.py
import re

from pathlib import Path

from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp

from custom_widgets import SuitButton
from constants import KV_DIR

LEAD_RE = r'^(10|[2-9JQKA])([SHDC♠♥♦♣])$'


_kv_loaded = False

def _load_kv():
    global _kv_loaded
    if not _kv_loaded:
        Builder.load_file(str(Path(KV_DIR, "lead_picker.kv")))
        _kv_loaded = True

_load_kv()

class LeadPicker(BoxLayout):
    """
    Phone-friendly lead picker for Bridge.
    Exposes `lead` StringProperty (e.g. "K♥", "A♠", "10♦")
    """
    lead = StringProperty("")
    parent_screen = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._level = ""
        self._suit = ""          # internal: S, H, D, C
        self._suit_label = ""    # display: ♠, ♥, ♦, ♣
        self._old_lead = ''

    # ==================================================================
    # Selection handlers (called from .kv)
    # ==================================================================
    def select_level(self, level: str):
        self._level = level
        self._highlight(self.ids.level_grid, level)
        if self._suit:
            self._update_display()

    def select_suit(self, suit: str, label: str):
        self._suit = suit
        self._suit_label = label
        self._highlight(self.ids.suit_grid, label)

        if self._level:
            self._update_display()

    # ==================================================================
    # Update display and property
    # ==================================================================
    def _update_display(self):
        if not (self._level and self._suit):
            return

        self.lead = f"{self._level}{self._suit}"

    # ==================================================================
    # Highlight selected button
    # ==================================================================
    def _highlight(self, grid, selected_text: str):
        for btn in grid.children:
            btn.selected = (btn.text == selected_text)

    # ==================================================================
    # Public method: Pre-fill when editing an existing board
    # ==================================================================
    def set_lead(self, lead: str):
        """Parse a lead like "K♥", "A♠", "10♦", "Q♣" and select it"""
        if not lead or lead == "—":
            self._level = self._suit = self._suit_label = ""
            self._update_display()
            return

        self._old_lead = lead
        # Improved regex: handles 2-9, 10, J,Q,K,A + suit symbol
        import re
        m = re.match(LEAD_RE, lead)
        if not m:
            print(f"[LeadPicker] Could not parse lead: {lead}")
            return

        level = m.group(1)
        suit_symbol = m.group(2)

        suit_map = {"♠": ("S", "♠"), "♥": ("H", "♥"),
                    "♦": ("D", "♦"), "♣": ("C", "♣")}

        if suit_symbol in suit_map:
            suit_code, label = suit_map[suit_symbol]
            self.select_level(level)
            self.select_suit(suit_code, label)
        else:
            print(f"[LeadPicker] Unknown suit symbol: {suit_symbol}")

    def reset(self):
        """Call this every time the picker is shown for a new selection."""
        self._level = ""
        self._suit = ""
        self._suit_label = ""
        self.lead = ""
        self._update_display()

        for grid in (self.ids.level_grid, self.ids.suit_grid):
            for btn in grid.children:
                btn.selected = False

    def cancel(self):
        self.lead = self._old_lead
        self.parent_screen._lead_modal.dismiss()

    def confirm(self):
        if not (self._level and self._suit):
            return
        value = f"{self._level}{self._suit}"
        self.parent_screen.commit(value)
        self.parent_screen._lead_modal.dismiss()
