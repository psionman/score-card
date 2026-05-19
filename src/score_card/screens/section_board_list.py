from pathlib import Path

from constants import KV_DIR
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.modalview import ModalView
from kivymd.uix.screen import MDScreen
from screens.board_row import BoardRow
from screens.score_picker import ScorePicker
from services.board import BoardService

Builder.load_file(str(Path(KV_DIR, "section_board_list.kv")))


class SectionBoardList(MDScreen):
    event = ObjectProperty(None, allownone=True)
    boards = ListProperty([])
    active_modal = None
    board = None

    def on_pre_enter(self):
        app = App.get_running_app()
        self.event = app.current_event
        self.load_boards()

    def load_boards(self):
        if not self.section:
            self.boards = []
            return
        boards = BoardService.get_boards_for_event(self.event.id)
        self.boards = [b for b in boards if b.section == self.section]

    def set_section(self, section):
        self.section = section

    def open_board(self, board):
        self.board = board
        self.open_modal("score")
        # score_picker = self.manager.get_screen("score_picker")
        # score_picker.set_board(board)
        # section_board_list.set_section(section)
        # self.manager.current = "section_board_list"

    def on_boards(self, instance, value):
        container = self.ids.board_list
        container.clear_widgets()

        # OPTIONAL HEADER
        container.add_widget(
            BoardRow(
                board="Board",
                score="Score",
                team_score="Team",
                imps="IMPs",
            )
        )

        for board in value:
            print(board)
            container.add_widget(
                BoardRow(
                    board=str(board.board_number),
                    score=str(board.score),
                    team_score=str(board.team_score),
                    imps=str(board.imps),
                )
            )

    def _enter_score(self):
        if not hasattr(self, "_score_modal"):
            self._score_modal = ModalView(
                size_hint=(1, None),
                height=dp(320),
                pos_hint={"bottom": 1},  # anchors to bottom of screen
                background_color=(0, 0, 0, 0.5),
                auto_dismiss=True,
            )
            self._score_modal.bind(on_dismiss=self._on_lead_modal_dismissed)
            self._score_modal.add_widget(self._score_picker)

        picker = self._score_picker
        picker.parent_screen = self
        picker.set_score(self.board.score)
        self._score_modal.open()

    def on_touch_up(self, touch):
        # only handle if NOT inside a picker
        if self.active_modal:
            picker = None

            if self.active_modal == "score":
                picker = self._score_picker

            if picker and picker.collide_point(*touch.pos):
                # let picker handle it
                return super().on_touch_up(touch)

            # otherwise ignore field triggers while modal open
            return True

        return super().on_touch_up(touch)

    def open_modal(self, name, field=None):
        print(name)
        if self.active_modal == name:
            return

        old = self.active_modal
        self.active_modal = name

        if old:
            self._close_modal(old)

        self._open_modal(name, field)

    def _open_modal(self, name, field):
        if name == "score":
            self._enter_score()

    def _close_modal(self, name):

        if name == "score":
            self.toggle_score_picker(False)

    def close_modal(self):
        if not self.active_modal:
            return

        self._close_modal(self.active_modal)
        self.active_modal = None

    # def commit(self, value):
    #     name = self.active_modal

    #     if name == "lead":
    #         self.ids.lead.text = value
    #     elif name == "contract":
    #         self.ids.contract.text = value
    #     elif name == "declarer":
    #         self.ids.declarer.text = value
    #     elif name == "tricks":
    #         self.ids.tricks.text = value
    #     elif name == "section":
    #         self.ids.section.text = value
    #     elif name == "orientation":
    #         self.ids.orientation.text = value
    #     elif name == "vulnerable":
    #         self.ids.vulnerable.text = value

    #     self.close_modal()

    def _on_score_modal_dismissed(self, *args):
        self.active_modal = None

    def _on_score_selected(self, _, value: str):
        # self.ids.lead.text = value
        print("score selected")

    def on_kv_post(self, base_widget):
        # Score modal
        self._score_modal = ModalView(
            size_hint=(1, None),
            height=dp(320),
            background_color=(0, 0, 0, 0.5),
            auto_dismiss=True,
        )
        self._score_modal.clear_widgets()

        def _position_bottom(modal, *args):
            modal.y = 0

        self._score_modal.bind(on_open=_position_bottom)
        self._score_modal.bind(on_dismiss=self._on_score_modal_dismissed)

        self._score_picker = ScorePicker(
            size_hint=(1, 1),
            parent_screen=self,
        )

        self._score_modal.add_widget(self._score_picker)
        self._score_picker.bind(score=self._on_score_selected)

    def save_section(self):
        print("save section")
