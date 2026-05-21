# screens/board_form.py
from pathlib import Path

from constants import KV_DIR
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.modalview import ModalView
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from scoring import calculate_score
from screens.contract_picker import ContractPicker
from screens.lead_picker import LeadPicker
from services.board import BoardService

Builder.load_file(str(Path(KV_DIR, "theme.kv")))
Builder.load_file(str(Path(KV_DIR, "board_form.kv")))

VUL_MAP = {
    "O": {"label": "None", "ns": False, "ew": False},
    "N": {"label": "NS", "ns": True, "ew": False},
    "E": {"label": "EW", "ns": False, "ew": True},
    "B": {"label": "Both", "ns": True, "ew": True},
}

SECTIONS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class BoardForm(MDScreen):
    board = ObjectProperty(None, allownone=True)
    orientation_default = "NS"
    contract = StringProperty("")
    lead = StringProperty("")
    active_picker = None  # "contract", "lead", etc.
    active_modal = None
    event = ObjectProperty(None, allownone=True)

    def on_pre_enter(self):
        app = App.get_running_app()
        self.event = app.current_event

    def open_menu(self, field, items):
        menu_items = [
            {
                "text": i,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i: self.set_item(field, x),
            }
            for i in items
        ]

        self.menu = MDDropdownMenu(
            caller=field,
            items=menu_items,
            width_mult=3,
        )
        self.menu.open()

    def set_item(self, field, value):
        field.text = value
        self.menu.dismiss()
        self.active_picker = None

    def set_board(self, board):
        self.board = board
        self.ids.contract.bind(text=self.recalculate)
        self.ids.declarer.bind(text=self.recalculate)
        self.ids.tricks.bind(text=self.recalculate)
        self.ids.vulnerable.bind(text=self.recalculate)
        self.ids.orientation.bind(text=self.recalculate)

        if not board:
            # New board → clear fields
            board_number = self.get_next_board_number()
            app = App.get_running_app()
            vulnerable = self.get_vulnerability(board_number)

            self.ids.board_number.text = str(board_number)
            self.ids.contract.text = ""
            self.ids.declarer.text = ""
            self.ids.tricks.text = ""
            self.ids.lead.text = ""
            self.ids.score.text = ""
            self.ids.vulnerable.text = VUL_MAP[vulnerable]["label"]
            self.ids.orientation.text = (
                app.last_board.orientation
                if app.last_board
                else self.orientation_default
            )
            self.ids.opponents.text = (
                str(app.last_board.opponents) if app.last_board else ""
            )
            self.ids.section.text = (
                app.last_board.section_id if app.last_board else "A"
            )
            self.ids.team_score.text = ""
            self.ids.imps.text = ""
            self.ids.notes_input.text = ""
            return

        # Edit mode → populate fields
        self.ids.board_number.text = str(board.board_number)
        self.ids.contract.text = board.contract or ""
        self.ids.declarer.text = board.declarer or ""
        self.ids.tricks.text = str(board.tricks)
        self.ids.lead.text = board.lead or ""
        self.ids.score.text = str(board.score)
        self.ids.vulnerable.text = board.vulnerable or ""
        self.ids.orientation.text = board.orientation or ""
        self.ids.opponents.text = str(board.opponents)
        self.ids.section.text = board.section or "A"
        self.ids.team_score.text = str(board.team_score)
        self.ids.imps.text = str(board.imps)
        self.ids.imps.notes_input = str(board.notes)

    def _get_previous_board(self) -> board:
        app = App.get_running_app()
        event = app.current_event
        boards = BoardService.get_boards_for_event(event.id) if event else []
        return boards[-1] if boards else None

    def get_next_board_number(self):
        app = App.get_running_app()
        event = app.current_event
        last_board = app.last_board if app.last_board else None

        if not event:
            return 1

        boards = BoardService.get_boards_for_event(event.id)

        if not boards:
            return 1

        board_ids = [int(board.board_number) for board in boards]
        next_board = last_board.board_number + 1 if last_board else 1
        while next_board in board_ids:
            next_board += 1

        return next_board

    def save_board(self):
        app = App.get_running_app()
        event = app.current_event

        data = {
            "board_number": int(self.ids.board_number.text or 0),
            "contract": self.ids.contract.text,
            "declarer": self.ids.declarer.text,
            "tricks": int(self.ids.tricks.text or 0),
            "lead": self.ids.lead.text,
            "score": int(self.ids.score.text or 0),
            "vulnerable": self.ids.vulnerable.text,
            "orientation": self.ids.orientation.text,
            "opponents": int(self.ids.opponents.text or 0),
            "section": self.ids.section.text,
            "team_score": int(self.ids.team_score.text or 0),
            "imps": int(self.ids.imps.text or 0),
            "notes": self.ids.notes_input.text,
        }

        if self.board:
            BoardService.update_board(self.board.id, **data)
        else:
            BoardService.create_board(
                event_id=event.id if event else None,
                **data,
            )
        app.set_last_board(
            [
                data["board_number"],
                data["orientation"],
                data["opponents"],
                data["section"],
            ]
        )
        app.nav.board_list("right")

    # Pickers
    def _show_menu(self, field, items):
        menu_items = [
            {
                "text": i,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i: self.commit(x),
            }
            for i in items
        ]

        self.menu = MDDropdownMenu(
            caller=field,
            items=menu_items,
            width_mult=3,
        )
        self.menu.bind(on_dismiss=self._on_menu_dismissed)
        self.menu.open()

    def _on_menu_dismissed(self, *args):
        old = self.active_modal
        self.active_modal = None
        self.menu = None
        self._close_modal(old)

    def _show_lead(self):
        self.ids.lead.focus = False

        if not hasattr(self, "_lead_modal"):
            self._lead_modal = ModalView(
                size_hint=(1, None),
                height=dp(320),
                pos_hint={"bottom": 1},  # anchors to bottom of screen
                background_color=(0, 0, 0, 0.5),
                auto_dismiss=True,
            )
            self._lead_modal.bind(on_dismiss=self._on_lead_modal_dismissed)
            self._lead_modal.add_widget(self._lead_picker)

        picker = self._lead_picker
        picker.parent_screen = self
        picker.set_lead(self.ids.lead.text)
        self._lead_modal.open()

    def on_touch_up(self, touch):
        # only handle if NOT inside a picker
        if self.active_modal:
            picker = None

            if self.active_modal == "lead":
                picker = self._lead_picker

            elif self.active_modal == "contract":
                picker = self.ids.contract_picker

            if picker and picker.collide_point(*touch.pos):
                # let picker handle it
                return super().on_touch_up(touch)

            # otherwise ignore field triggers while modal open
            return True

        return super().on_touch_up(touch)

    def open_modal(self, name, field=None):
        if self.active_modal == name:
            return

        old = self.active_modal
        self.active_modal = name

        if old:
            self._close_modal(old)

        self._open_modal(name, field)

    def _open_modal(self, name, field):
        if name == "lead":
            self._show_lead()
        elif name == "contract":
            self._show_contract()
        elif name == "declarer":
            self._show_menu(field, ["N", "S", "E", "W"])
        elif name == "tricks":
            self._show_menu(field, [str(_) for _ in reversed(range(14))])
        elif name == "section":
            self._show_menu(field, [section for section in SECTIONS])
        elif name == "orientation":
            self._show_menu(field, ["NS", "EW"])
        elif name == "vulnerable":
            self._show_menu(field, ["None", "NS", "EW", "Both"])

    def _close_modal(self, name):
        if name in [
            "declarer",
            "orientation",
            "vulnerable",
            "tricks",
            "section",
        ]:
            self.close_menu()

        elif name == "lead":
            self.toggle_lead_picker(False)

        elif name == "contract":
            if hasattr(self, "_contract_modal"):
                self._contract_modal.dismiss()

    def close_modal(self):
        if not self.active_modal:
            return

        self._close_modal(self.active_modal)
        self.active_modal = None

    def commit(self, value):
        name = self.active_modal

        if name == "lead":
            self.ids.lead.text = value
        elif name == "contract":
            self.ids.contract.text = value
        elif name == "declarer":
            self.ids.declarer.text = value
        elif name == "tricks":
            self.ids.tricks.text = value
        elif name == "section":
            self.ids.section.text = value
        elif name == "orientation":
            self.ids.orientation.text = value
        elif name == "vulnerable":
            self.ids.vulnerable.text = value

        self.close_modal()

    def close_menu(self):
        if hasattr(self, "menu") and self.menu:
            self.menu.dismiss()
            self.menu = None
        self.active_picker = None

    def get_vulnerability(self, board_number: int) -> str:
        b = board_number - 1
        code = (b + b // 4) % 4
        return ["O", "N", "E", "B"][code]

    def on_board_number_changed(self, value):
        try:
            board_number = int(value)
        except ValueError:
            return  # ignore incomplete input like "" or "-"
        vulnerable = self.get_vulnerability(board_number)
        self.ids.vulnerable.text = VUL_MAP[vulnerable]["label"]

    def on_kv_post(self, base_widget):
        # Lead modal
        self._lead_modal = ModalView(
            size_hint=(1, None),
            height=dp(320),
            background_color=(0, 0, 0, 0.5),
            auto_dismiss=True,
        )
        self._lead_modal.clear_widgets()

        def _position_bottom(modal, *args):
            modal.y = 0

        self._lead_modal.bind(on_open=_position_bottom)
        self._lead_modal.bind(on_dismiss=self._on_lead_modal_dismissed)

        self._lead_picker = LeadPicker(
            size_hint=(1, 1),
            parent_screen=self,
        )

        self._lead_modal.add_widget(self._lead_picker)
        self._lead_picker.bind(lead=self._on_lead_selected)

        # Contract modal
        self._contract_modal = ModalView(
            size_hint=(1, None),
            height=dp(320),
            background_color=(0, 0, 0, 0.5),
            auto_dismiss=True,
        )
        self._contract_modal.bind(on_open=_position_bottom)
        self._contract_modal.bind(on_dismiss=self._on_contract_modal_dismissed)

        self._contract_picker = ContractPicker(
            size_hint=(1, 1), parent_screen=self
        )
        self._contract_modal.add_widget(self._contract_picker)
        self._contract_picker.bind(contract=self._on_contract_selected)

    def _hide_card(self, card, picker) -> None:
        card.opacity = 0
        card.disabled = True
        card.height = 0
        card.padding = 0
        picker.height = 0

    # Contract
    def _show_contract(self):
        self.ids.contract.focus = False
        self._contract_picker.parent_screen = self
        self._contract_picker.reset()
        self._contract_picker.set_contract(self.ids.contract.text)
        self._contract_modal.open()

    def _hide_contract_picker(self):
        self.toggle_contract_picker(False)

    def toggle_contract_picker(self, focused: bool):
        if focused:
            self._show_contract()
        else:
            if hasattr(self, "_contract_modal"):
                self._contract_modal.dismiss()

    def _on_contract_selected(self, _, value: str):
        self.ids.contract.text = value

    def _on_contract_modal_dismissed(self, *args):
        self.active_modal = None

    # Lead
    def toggle_lead_picker(self, focused: bool):
        if focused:
            self._show_lead()
        else:
            if hasattr(self, "_lead_modal"):
                self._lead_modal.dismiss()

    def _on_lead_selected(self, _, value: str):
        self.ids.lead.text = value

    def _on_lead_modal_dismissed(self, *args):
        self.active_modal = None

    # Score
    def recalculate(self, *args):
        contract = self.ids.contract.text.strip()
        declarer = self.ids.declarer.text.strip()
        vulnerable = self.ids.vulnerable.text.strip()
        tricks_text = self.ids.tricks.text.strip()
        orientation = self.ids.orientation.text.strip()

        # Require all fields (but tricks can be "0")
        if (
            not contract
            or not declarer
            or not vulnerable
            or not orientation
            or tricks_text == ""
        ):
            self.ids.score.text = ""
            self.ids.imps.text = ""
            return

        try:
            tricks = int(tricks_text)
        except ValueError:
            return  # still typing invalid number

        our_contract = declarer in orientation
        score = calculate_score(
            contract, declarer, tricks, vulnerable, our_contract
        )
        self.ids.score.text = str(score)

        # imps = self.calculate_imps(score)
        # self.ids.imps.text = str(imps)

    def on_touch_down(self, touch):
        if self.active_modal:
            # find the active picker widget
            if self.active_modal in ["lead", "contract"]:
                return True  # swallow all touches — modal handles its own
            else:
                picker_card = None

            if picker_card and picker_card.collide_point(*touch.pos):
                # let the picker handle it normally
                return super().on_touch_down(touch)

            # swallow everything else
            return True

        return super().on_touch_down(touch)
