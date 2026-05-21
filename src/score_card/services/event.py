# /services/event.py

from models.event import Event
from repositories.board import BoardRepository
from repositories.event import EventRepository
from services.partner import PartnerService


class EventService:
    @staticmethod
    def create_event(name, date, partner_id, location="", notes=""):
        return EventRepository.create(
            name=name,
            date=date,
            partner_id=partner_id,
            location=location,
            notes=notes,
        )

    @staticmethod
    def get_event(event_id):
        row = EventRepository.get_by_id(event_id)
        if not row:
            return None

        event_id, name, date, partner_id, location, notes = row

        partner = PartnerService.get_partner(partner_id)
        boards = BoardRepository.get_by_event(event_id)

        return Event(
            id=event_id,
            name=name,
            date=date,
            partner_id=partner_id,
            location=location,
            notes=notes,
            boards=boards,
        )

    @staticmethod
    def list_events():
        rows = EventRepository.get_all()

        events = []
        for r in rows:
            event_id, name, date, partner_id, location, notes = r

            partner = PartnerService.get_partner(partner_id)

            events.append(
                Event(
                    id=event_id,
                    name=name,
                    date=date,
                    partner_id=partner_id,
                    location=location,
                    notes=notes,
                    boards=[],
                )
            )

        return events

    @staticmethod
    def update_event(event_id, name, date, partner_id, location="", notes=""):
        EventRepository.update(
            event_id=event_id,
            name=name,
            date=date,
            partner_id=partner_id,
            location=location,
            notes=notes,
        )

        return EventService.get_event(event_id)

    @staticmethod
    def add_board(event_id, board_name):
        return BoardRepository.create(event_id, board_name)

    @staticmethod
    def delete_event(event_id):
        EventRepository.delete(event_id)
