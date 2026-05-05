# screens/event-list.py
from pathlib import Path

from constants import KV_DIR
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.list import OneLineListItem
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty

from custom_widgets import (
    IconListItem, menu_divider, menu_icon_item, menu_handler)

from services.event import EventService
from services.partner import PartnerService


Builder.load_file(str(Path(KV_DIR, "theme.kv")))
Builder.load_file(str(Path(KV_DIR, "event_list.kv")))


class EventList(MDScreen):
    def on_pre_enter(self):
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

    def go_settings_form(self):
        form = self.manager.get_screen("settings_form")
        # form.set_event(None)
        App.get_running_app().nav.settings_form()

    def go_partners(self):
        App.get_running_app().nav.partner_list()

    def go_home(self):
        App.get_running_app().nav.home()

    def open_menu(self, caller):
        menu_items = [
            menu_icon_item("Partners", "account-group", self.select_menu),
            menu_divider,
            menu_icon_item("Settings", "cog", self.select_menu),
        ]
        self.menu = menu_handler(caller, menu_items)

    def select_menu(self, item):
        if hasattr(self, "menu") and self.menu:
            self.menu.dismiss()

        if item == "Partners":
            self.go_partners()

        elif item == "Settings":
            self.go_settings_form()
