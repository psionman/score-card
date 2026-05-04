# navigation.py
class NavigationService:
    def __init__(self, screen_manager):
        self.sm = screen_manager

    def go(self, screen_name, direction="left"):
        self.sm.transition.direction = direction
        self.sm.current = screen_name

    def home(self):
        self.go("event_list", direction="right")

    def event_form(self):
        self.go("event_form")

    def partner_form(self):
        self.go("partner_form")

    def partner_list(self):
        self.go("partner_list")

    def boards(self):
        self.go("board_list")

    def board_form(self):
        self.go("board_form")

    def settings_form(self):
        self.go("settings_form")
