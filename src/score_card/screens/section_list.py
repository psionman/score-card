from kivy.properties import ObjectProperty, ListProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem
from kivy.lang import Builder
from kivy.app import App

from pathlib import Path

from constants import KV_DIR
from services.board import BoardService

Builder.load_file(str(Path(KV_DIR, "section_list.kv")))


class SectionList(MDScreen):
    event = ObjectProperty(None, allownone=True)
    sections = ListProperty([])
    section_boards = {}

    def on_pre_enter(self):
        app = App.get_running_app()
        self.event = app.current_event
        self.load_boards()

    def load_boards(self):
        if not self.event:
            self.sections = []
            return
        boards = BoardService.get_boards_for_event(self.event.id)

        sections = []
        for board in boards:
            if board.section and board.section not in sections:
                sections.append(board.section)
            self.section_boards.setdefault(board.section, []).append(board)
        self.sections = sorted(sections)

    def open_section(self, section):
        section_board_list = self.manager.get_screen("section_board_list")
        section_board_list.set_section(section)
        self.manager.current = "section_board_list"

    def on_sections(self, instance, value):
        self.ids.section_list.clear_widgets()

        for section in value:
            item = OneLineListItem(text=(f"Section {section}"))
            item.bind(on_release=lambda x, s=section: self.open_section(s))
            self.ids.section_list.add_widget(item)
