# navigation.py
from kivy.uix.screenmanager import SlideTransition


class NavigationService:
    def __init__(self, screen_manager):
        self.sm = screen_manager
        self.sm.transition = SlideTransition()

    def go(self, screen_name, direction="left"):
        self.sm.transition.direction = direction
        self.sm.current = screen_name

    def event_list(self, direction="right"):
        self.go("event_list", direction=direction)

    def event_form(self, direction="left"):
        self.go("event_form", direction=direction)

    def partner_form(self):
        self.go("partner_form")

    def partner_list(self):
        self.go("partner_list")

    def board_list(self, direction="left"):
        self.go("board_list", direction=direction)

    def section_list(self, direction="left"):
        self.go("section_list", direction=direction)

    def section_board_list(self, direction="left"):
        self.go("section_board_list", direction=direction)

    def board_form(self):
        self.go("board_form")

    def settings_form(self):
        self.go("settings_form")
