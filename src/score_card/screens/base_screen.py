from kivymd.uix.screen import MDScreen


class BaseScreen(MDScreen):
    def go_home(self):
        self.manager.transition.direction = "right"
        self.manager.current = "home"
