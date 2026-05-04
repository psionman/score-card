# screens/settings_form.py

from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from pathlib import Path

from services.settings import SettingsService
from constants import KV_DIR

Builder.load_file(str(Path(KV_DIR, "settings_form.kv")))


class SettingsFormScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        settings = SettingsService.get_settings(1)
        self.set_settings(settings)


    def set_settings(self, settings):
        self.settings = settings

        if settings:
            self.ids.email_input.text = settings.email_address
        else:
            self.ids.email_input.text = ""

    def save(self):
        email_address = self.ids.email_input.text

        try:
            if self.settings:
                SettingsService.update_settings(self.settings.id, email_address)
            else:
                SettingsService.create_settings(email_address)

            self.manager.current = "settings_form"

        except ValueError as e:
            self.show_error(str(e))

    def show_error(self, message):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton

        self.dialog = MDDialog(
            title="Error",
            text=message,
            buttons=[
                MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())
            ],
        )
        self.dialog.open()
