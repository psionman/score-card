from pathlib import Path

from constants import KV_DIR
from kivy.lang import Builder
from kivymd.uix.list import OneLineListItem
from kivymd.uix.screen import MDScreen
from services.export import export_partners_csv
from services.partner import PartnerService

Builder.load_file(str(Path(KV_DIR, "partner_list.kv")))


class PartnerListScreen(MDScreen):
    partners = None

    def on_pre_enter(self):
        self.partners = self.load_partners()

    def load_partners(self):
        self.ids.partner_list.clear_widgets()

        partners = PartnerService.list_partners()

        for p in partners:
            item = OneLineListItem(
                text=f"{p.name} ({p.ebu_number})",
                on_release=lambda x, partner=p: self.edit_partner(partner),
            )
            self.ids.partner_list.add_widget(item)
        return partners

    def add_partner(self):
        self.manager.get_screen("partner_form").set_partner(None)
        self.manager.current = "partner_form"

    def edit_partner(self, partner):
        self.manager.get_screen("partner_form").set_partner(partner)
        self.manager.current = "partner_form"

    def export_csv(self):
        # partners = PartnerService.list_partners()
        # path = export_partners_csv(partners)
        # show_message('Export partners', f"Saved in :\n{path.name}")

        export_partners_csv(self.partners)
