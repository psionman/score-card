# screens/conmtract_picker.py
import re
from pathlib import Path

from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.app import MDApp

from custom_widgets import SuitButton
from constants import KV_DIR

_kv_loaded = False

def _load_kv():
    global _kv_loaded
    if not _kv_loaded:
        Builder.load_file(str(Path(KV_DIR, "contract_picker.kv")))
        _kv_loaded = True

_load_kv()


class ContractPicker(BoxLayout):
    """
    A phone-friendly contract picker.
    Exposes a `contract` StringProperty that updates as the user taps.
    Bind to this in BoardForm:
        self.ids.contract_picker.bind(contract=self.on_contract_changed)
    """

    contract = StringProperty("")
    parent_screen = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._level  = ""
        self._suit   = ""
        self._suit_label = ""
        self._doubled = ""

    def select_level(self, level: str):
        if level == 'P':
            self.reset()
        self._level = level
        is_passout = level == "P"
        self.ids.suit_grid.disabled   = is_passout
        self.ids.doubled_grid.disabled = is_passout
        if is_passout:
            self._suit   = ""
            self._doubled = ""
        self._highlight(self.ids.level_grid,  level)

    def select_suit(self, suit: str, label: str):
        self._suit       = suit
        self._suit_label = label
        self._highlight(self.ids.suit_grid, label)


    def select_doubled(self, doubled: str):
        self._doubled = doubled
        self._highlight(self.ids.doubled_grid, doubled)

    def _highlight(self, grid, selected_text: str):
        for btn in grid.children:
            btn.selected = False
            if isinstance(btn, SuitButton):
                btn.selected = (btn.text == selected_text)

    def set_contract(self, contract: str):
        """Parse a contract string back into level / suit / doubled."""
        if not contract:
            return

        if contract == "P":
            self.select_level("P")
            self._suit = ''
            return

        m = re.match(r'^([1-7])(S|H|D|C|NT)(X{0,2})$', contract, re.IGNORECASE)
        if not m:
            return

        level, suit, doubled = m.group(1), m.group(2).upper(), m.group(3).upper()
        suit_labels = {"S": "♠", "H": "♥", "D": "♦", "C": "♣", "NT": "NT"}

        self.select_level(level)
        self.select_suit(suit, suit_labels.get(suit, suit))
        self.select_doubled(doubled)

    def reset(self):
        self._level = ""
        self._suit = ""
        self._suit_label = ""
        self._doubled = ""
        self.contract = ""
        for grid in (self.ids.level_grid, self.ids.suit_grid, self.ids.doubled_grid):
            for btn in grid.children:
                if isinstance(btn, SuitButton):
                    btn.selected = False

    def cancel(self):
        self.parent_screen._contract_modal.dismiss()

    def confirm(self):
        if self._level != 'P' and not (self._level and self._suit):
            return

        if self._level == 'P':
            self._suit = ''

        doubled = self._doubled if self._doubled in ['X', 'XX'] else ''
        contract = f'{self._level}{self._suit}{doubled}'

        self.parent_screen.commit(contract)
        self.parent_screen._contract_modal.dismiss()
