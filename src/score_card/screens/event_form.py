from pathlib import Path
from datetime import datetime

from kivy.app import App
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window

from constants import KV_DIR
from services.event import EventService
from services.partner import PartnerService
from screens.base_screen import BaseScreen

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
        textfield.focus = False  # 🔥 IMPORTANT

        def on_save(instance, value, date_range):
            textfield.text = value.strftime("%Y-%m-%d")

        def on_cancel(instance, value):
            pass

        date_dialog = MDDatePicker()

        if textfield.text:
            try:
                initial_date = datetime.strptime(textfield.text, "%Y-%m-%d").date()
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
            Clock.schedule_once(lambda dt: self._open_partner_menu(widget), 0.3)
            return True
        return False

    def set_partner(self, partner):
        self.selected_partner = partner
        self.ids.partner_input.text = f"{partner.name} ({partner.ebu_number})"

        if self.partner_menu:
            self.partner_menu.dismiss()

    def save_event(self):
        if not self.selected_partner:
            self.show_snackbar("Partner is required")
            return

        name = self.ids.name_input.text
        date = self.ids.date_input.text
        notes = self.ids.notes_input.text

        if not name or not date:
            self.show_snackbar("Name and Date are required")
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
            EventService.create_event(
                name=name,
                date=date,
                partner_id=self.selected_partner.id,
                notes=notes,
            )

        # 🔥 Always reset form state
        self.set_event(None)

        # 🔥 Navigate away (don’t keep stale state)
        self.manager.transition.direction = "right"
        self.manager.current = "event_list"

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

        # 🔥 IMPORTANT: load partner properly
        partner = PartnerService.get_partner(event.partner_id)

        if partner:
            self.selected_partner = partner
            self.ids.partner_input.text = f"{partner.name} ({partner.ebu_number})"
        else:
            # fallback safe state
            self.selected_partner = None
            self.ids.partner_input.text = "Unknown Partner"

        # display ONLY
        # self.ids.partner_input.text = f"{partner.name} ({partner.ebu_number})"

    def go_boards(self):
        if not self.event:
            return

        # screen = self.manager.get_screen("board_list")
        # screen.event = self.event   # 👈 CRITICAL
        # self.manager.current = "board_list"

        app = App.get_running_app()
        app.set_event(self.event)  # store current event globally if needed
        app.nav.boards()



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
