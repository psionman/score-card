from kivy.properties import ObjectProperty, ListProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem
from kivy.lang import Builder
from kivy.app import App
from kivymd.toast import toast

from pathlib import Path

from constants import KV_DIR
from services.board import BoardService
from services.export import export_event_csv
from utilities import show_message

Builder.load_file(str(Path(KV_DIR, "board_list.kv")))

class BoardList(MDScreen):
    event = ObjectProperty(None, allownone=True)
    boards = ListProperty([])

    def on_pre_enter(self):
        app = App.get_running_app()
        self.event = app.current_event
        self.load_boards()

    def load_boards(self):
        if not self.event:
            self.boards = []
            return
        self.boards = BoardService.get_boards_for_event(self.event.id)

    def go_add_board(self):
        form = self.manager.get_screen("board_form")
        form.set_board(None)
        App.get_running_app().nav.board_form()

    def open_board(self, board):
        print("Open board:", board)
        board_form = self.manager.get_screen("board_form")
        board_form.set_board(board)
        self.manager.current = "board_form"

    def on_boards(self, instance, value):
        self.ids.board_list.clear_widgets()

        for board in value:
            item = OneLineListItem(
                text=(f"Board {board.board_number} - {board.contract} "
                      f"by {board.declarer}: {board.score}")
            )
            item.bind(on_release=lambda x, b=board: self.open_board(b))
            self.ids.board_list.add_widget(item)

    def export_csv(self):
        self.event.boards = BoardService.get_boards_for_event(self.event.id)
        path = export_event_csv(self.event)
        # show a toast/snackbar
        # toast(f"Saved to {path}")?
        show_message('Export Event', f"Saved in :\n{path.name}")
