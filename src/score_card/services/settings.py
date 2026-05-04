# services/settings.py
from models.settings import Settings
from repositories.settings import SettingsRepository


class SettingsService:
    @staticmethod
    def _validate(email_address: str):
        # if not ebu_number.isdigit():
        #     raise ValueError("EBU number must be numeric")
        ...

    @staticmethod
    def create_settings(email_address: str):
        SettingsService._validate(email_address)

        return SettingsRepository.create(email_address)

    @staticmethod
    def get_settings(settings_id: int):
        row = SettingsRepository.get_by_id(settings_id)

        if not row:
            return None

        settings_id, email_address= row

        return Settings(id=settings_id, email_address=email_address)

    @staticmethod
    def list_settingss():
        rows = SettingsRepository.get_all()

        return [Settings(id=r[0], email_address=r[1], ebu_number=r[2]) for r in rows]

    @staticmethod
    def update_settings(settings_id: int, email_address: str):
        SettingsService._validate(email_address)

        existing = SettingsRepository.get_by_id(settings_id)
        if not existing:
            raise ValueError("Settings not found")

        SettingsRepository.update(settings_id, email_address)

    # SAFE DELETE
    @staticmethod
    def delete_settings(settings_id: int):
        # Prevent deleting if used by events
        from app.db.connection import get_connection

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT COUNT(*) FROM events WHERE settings_id = ?
        """,
            (settings_id,),
        )

        count = cur.fetchone()[0]
        conn.close()

        if count > 0:
            raise ValueError("Cannot delete settings: used by events")

        SettingsRepository.delete(settings_id)
