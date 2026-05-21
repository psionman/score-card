from datetime import datetime
from pathlib import Path

from constants import KV_DIR
from custom_widgets import menu_handler, menu_icon_item
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker
from screens.base_screen import BaseScreen
from services.event import EventService
from services.export import export_event_csv
from services.partner import PartnerService
from utilities import error_dialog

Builder.load_file(str(Path(KV_DIR, "theme.kv")))
Builder.load_file(str(Path(KV_DIR, "event_form.kv")))


class EventForm(BaseScreen):
    event = ObjectProperty(None, allownone=True)
    selected_partner = ObjectProperty(None, allownone=True)
    partner_menu = ObjectProperty(None, allownone=True)

    active_modal = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def handle_date_touch(self, widget, touch):
        if widget.collide_point(*touch.pos):
            widget.focus = False

            self.show_date_picker(widget)
            return True
        return False

    def show_date_picker(self, textfield):
        textfield.focus = False

        def on_save(instance, value, date_range):
            textfield.text = value.strftime("%Y-%m-%d")

        def on_cancel(instance, value):
            pass

        date_dialog = MDDatePicker()

        if textfield.text:
            try:
                initial_date = datetime.strptime(
                    textfield.text, "%Y-%m-%d"
                ).date()
                date_dialog.year = initial_date.year
                date_dialog.month = initial_date.month
                date_dialog.day = initial_date.day
            except:
                pass

        date_dialog.bind(on_save=on_save, on_cancel=on_cancel)
        date_dialog.open()

    def open_partner_menu(self, caller):
        # ⬇️ Defer execution to next frame (prevents Android crash)
        Clock.schedule_once(lambda dt: self._open_partner_menu(caller), 0.3)

    def _open_partner_menu(self, caller):
        Window.release_all_keyboards()

        partners = PartnerService.list_partners()
        if not partners:
            self.ids.partner_input.text = "No partners available"
            return

        menu_items = []

        for p in partners:
            menu_items.append(
                {
                    "text": f"{p.name}",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=p: self.set_partner(x),
                }
            )

        if self.partner_menu:
            self.partner_menu.dismiss()

        self.partner_menu = MDDropdownMenu(
            caller=caller,
            items=menu_items,
            width_mult=4,
        )

        self.partner_menu.open()

    def handle_partner_touch(self, widget, touch):
        if widget.collide_point(*touch.pos):
            widget.focus = False
            Window.release_all_keyboards()
            Clock.schedule_once(
                lambda dt: self._open_partner_menu(widget), 0.3
            )
            return True
        return False

    def set_partner(self, partner):
        self.selected_partner = partner
        self.ids.partner_input.text = f"{partner.name} ({partner.ebu_number})"

        if self.partner_menu:
            self.partner_menu.dismiss()

    def save_event(self):
        name = self.ids.name_input.text
        date = self.ids.date_input.text
        notes = self.ids.notes_input.text

        if not name or not date or not self.selected_partner:
            error_dialog(
                "Name and Date and Partner are required",
                "Please fill in all required fields",
            )
            return

        if self.event:
            # EDIT
            EventService.update_event(
                event_id=self.event.id,
                name=name,
                date=date,
                partner_id=self.selected_partner.id,
                notes=notes,
            )
        else:
            # CREATE
            event_id = EventService.create_event(
                name=name,
                date=date,
                partner_id=self.selected_partner.id,
                notes=notes,
            )
            self.event = EventService.get_event(event_id)

    def set_event(self, event):
        self.event = event

        if not event:
            self.ids.name_input.text = ""
            self.ids.date_input.text = ""
            self.ids.partner_input.text = ""
            self.ids.notes_input.text = ""
            self.selected_partner = None
            return

        # basic fields
        self.ids.name_input.text = event.name
        self.ids.date_input.text = event.date
        self.ids.notes_input.text = event.notes or ""

        partner = PartnerService.get_partner(event.partner_id)

        if partner:
            self.selected_partner = partner
            self.ids.partner_input.text = (
                f"{partner.name} ({partner.ebu_number})"
            )
        else:
            # fallback safe state
            self.selected_partner = None
            self.ids.partner_input.text = "Unknown Partner"

    def go_boards(self):
        if not self.event:
            return

        app = App.get_running_app()
        app.set_event(self.event)
        app.nav.board_list()

    def go_sections(self):
        if not self.event:
            return

        app = App.get_running_app()
        app.set_event(self.event)
        app.nav.section_list()

    def event_delete(self):
        if not self.event:
            return

        dialog = MDDialog(
            title="Delete Event",
            text=f"Are you sure you want to delete '{self.event.name}'?",
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: dialog.dismiss(),
                ),
                MDFlatButton(
                    text="DELETE",
                    on_release=lambda x: self._confirm_delete(dialog),
                ),
            ],
        )

        dialog.open()

    def _confirm_delete(self, dialog):
        dialog.dismiss()

        EventService.delete_event(self.event.id)

        self.event = None
        self.set_event(None)

        app = App.get_running_app()
        app.nav.event_list("right")

    def open_modal(self, name, field=None):
        if self.active_modal == name:
            return

        old = self.active_modal
        self.active_modal = name

        if old:
            self._close_modal(old)

        self._open_modal(name, field)

    def _open_modal(self, name, field):
        self.open_partner_menu(field)

    def _close_modal(self, name):
        self.close_menu()

    def close_modal(self):
        if not self.active_modal:
            return

        self._close_modal(self.active_modal)
        self.active_modal = None

    def open_menu(self, caller):
        menu_items = [
            menu_icon_item("Save", "content-save", self.select_menu),
            menu_icon_item("Boards", "playlist-plus", self.select_menu),
            menu_icon_item("Sections", "trophy", self.select_menu),
            menu_icon_item("Export", "export", self.select_menu),
            menu_icon_item("Delete", "trash-can-outline", self.select_menu),
        ]
        self.menu = menu_handler(caller, menu_items)

    def select_menu(self, item):
        if hasattr(self, "menu") and self.menu:
            self.menu.dismiss()

        if item == "Save":
            self.save_event()

        elif item == "Boards":
            self.go_boards()

        elif item == "Sections":
            self.go_sections()

        elif item == "Export":
            export_event_csv(self.event)

        elif item == "Delete":
            self.event_delete()
