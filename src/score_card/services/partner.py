# services/partner.py
from models.partner import Partner
from repositories.partner import PartnerRepository


class PartnerService:
    @staticmethod
    def _validate(name: str, ebu_number: str):
        if not ebu_number.isdigit():
            raise ValueError("EBU number must be numeric")

    @staticmethod
    def create_partner(name: str, ebu_number: str):
        PartnerService._validate(name, ebu_number)

        return PartnerRepository.create(name, ebu_number)

    @staticmethod
    def get_partner(partner_id: int):
        row = PartnerRepository.get_by_id(partner_id)

        if not row:
            return None

        partner_id, name, ebu_number = row

        return Partner(id=partner_id, name=name, ebu_number=ebu_number)

    @staticmethod
    def list_partners():
        rows = PartnerRepository.get_all()

        return [Partner(id=r[0], name=r[1], ebu_number=r[2]) for r in rows]

    @staticmethod
    def update_partner(partner_id: int, name: str, ebu_number: str):
        PartnerService._validate(name, ebu_number)

        existing = PartnerRepository.get_by_id(partner_id)
        if not existing:
            raise ValueError("Partner not found")

        PartnerRepository.update(partner_id, name, ebu_number)

    # SAFE DELETE
    @staticmethod
    def delete_partner(partner_id: int):
        # Prevent deleting if used by events
        from app.db.connection import get_connection

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT COUNT(*) FROM events WHERE partner_id = ?
        """,
            (partner_id,),
        )

        count = cur.fetchone()[0]
        conn.close()

        if count > 0:
            raise ValueError("Cannot delete partner: used by events")

        PartnerRepository.delete(partner_id)
