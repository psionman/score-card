from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from pathlib import Path

from services.partner import PartnerService
from constants import KV_DIR

Builder.load_file(str(Path(KV_DIR, "partner_form.kv")))


class PartnerFormScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.partner = None

    def set_partner(self, partner):
        self.partner = partner

        if partner:
            self.ids.name_input.text = partner.name
            self.ids.ebu_input.text = partner.ebu_number
        else:
            self.ids.name_input.text = ""
            self.ids.ebu_input.text = ""

    def save(self):
        name = self.ids.name_input.text
        ebu = self.ids.ebu_input.text

        try:
            if self.partner:
                PartnerService.update_partner(self.partner.id, name, ebu)
            else:
                PartnerService.create_partner(name, ebu)

            self.manager.current = "partner_list"

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
