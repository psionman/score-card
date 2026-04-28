from pathlib import Path
from kivymd.uix.list import OneLineListItem
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivymd.uix.menu import MDDropdownMenu
from kivy.lang import Builder
from kivy.app import App
from kivy.metrics import dp


from services.event import EventService
from services.partner import PartnerService

from constants import KV_DIR

Builder.load_file(str(Path(KV_DIR, "theme.kv")))
Builder.load_file(str(Path(KV_DIR, "event_list.kv")))


class EventList(MDScreen):
    def on_pre_enter(self):
        # if self.event:
        #     self.set_event(self.event)
        self.load_events()

    def load_events(self):
        self.ids.event_list.clear_widgets()

        events = EventService.list_events()
        if not events:
            self.ids.event_list.add_widget(OneLineListItem(text="No events yet"))
            return

        for event in events:
            partner = PartnerService.get_partner(event.partner_id)
            item = OneLineListItem(
                text=f"{event.date} - {event.name} ({partner.name})",
                on_release=lambda x, e=event: self.open_event(e),
            )

            self.ids.event_list.add_widget(item)

    def open_event(self, event):
        form = self.manager.get_screen("event_form")
        form.set_event(event)

        self.manager.transition.direction = "left"
        self.manager.current = "event_form"



    def go_event_form(self):
        form = self.manager.get_screen("event_form")
        form.set_event(None)
        App.get_running_app().nav.event_form()

    def go_partners(self):
        App.get_running_app().nav.partner_list()

    def go_home(self):
        App.get_running_app().nav.home()

    def open_menu(self, caller):
        menu_items = [
            {
                "text": "Partners",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Partners": self.select_menu("partners"),
            },
            # {
            #     "viewclass": "Divider",
            #     "height": dp(1),
            #     "on_release": lambda: None,
            # },
            # {
            #     "text": "Restore from Download",
            #     "viewclass": "OneLineListItem",
            #     "on_release": lambda x="Restore": restore_from_download(self),
            # },
            # {
            #     "text": "Backup DB",
            #     "viewclass": "OneLineListItem",
            #     "on_release": backup_db,
            # },
            # {
            #     "text": "Restore DB",
            #     "viewclass": "OneLineListItem",
            #     "on_release": restore_db,
            # },
        ]
        self.menu = MDDropdownMenu(
            caller=caller,
            items=menu_items,
            width_mult=4,
        )
        self.menu.open()

    def select_menu(self, item):
        if hasattr(self, "menu") and self.menu:
            self.menu.dismiss()

        if item == "partners":
            self.go_partners()

        # elif item == "events":
        #     self.refresh_events()
