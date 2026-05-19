from pathlib import Path

from constants import KV_DIR
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty, ObjectProperty
from kivymd.uix.list import OneLineListItem
from kivymd.uix.screen import MDScreen
from services.board import BoardService

Builder.load_file(str(Path(KV_DIR, "section_list.kv")))


class SectionList(MDScreen):
    event = ObjectProperty(None, allownone=True)
    sections = ListProperty([])
    section_boards = {}
    section_imps = {}

    def on_pre_enter(self):
        app = App.get_running_app()
        self.event = app.current_event
        self.load_boards()

    def load_boards(self):
        if not self.event:
            self.sections = []
            return
        self.boards = BoardService.get_boards_for_event(self.event.id)
        self.sections = self.get_sections()

    def get_sections(self) -> list:
        sections = []
        self.section_imps = {}
        for board in self.boards:
            if board.section and board.section not in sections:
                sections.append(board.section)
            if board.section and board.section not in self.section_imps:
                self.section_imps[board.section] = 0
            self.section_boards.setdefault(board.section, []).append(board)
            self.section_imps[board.section] += board.imps
        return sorted(sections)

    def open_section(self, section):
        section_board_list = self.manager.get_screen("section_board_list")
        section_board_list.set_section(section)
        section_board_list.set_parent(self)
        self.manager.current = "section_board_list"

    def on_sections(self, instance, value):
        self.display_sections(value)

    def update_sections(self):
        self.display_sections(self.sections)

    def display_sections(self, sections: list) -> None:
        self.ids.section_list.clear_widgets()
        self.boards = BoardService.get_boards_for_event(self.event.id)

        self.sections = self.get_sections()
        for section in sections:
            imps = self.section_imps[section]
            item = OneLineListItem(text=(f"Section {section} {imps}"))
            item.bind(on_release=lambda x, s=section: self.open_section(s))
            self.ids.section_list.add_widget(item)
