# services/export.py
import csv
import logging
import traceback
from pathlib import Path

from kivy.app import App
from kivy.utils import platform
from models.event import Event
from services.board import BoardService
from services.partner import PartnerService
from utilities import msg_dialog


def export_event_csv(event: Event) -> str:
    downloads = _get_download_dir()

    safe_name = event.name.replace(" ", "_").replace("/", "-")
    filename = f"{event.date}_{safe_name}.csv"

    filepath = downloads / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)

    event.boards = BoardService.get_boards_for_event(event.id)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # -----------------------
        # EVENT DETAILS
        # -----------------------

        writer.writerow(["Event Name", event.name])
        writer.writerow(["Date", event.date])
        writer.writerow(["Location", event.location or ""])
        writer.writerow(["Notes", event.notes or ""])
        writer.writerow([])

        partner = PartnerService.get_partner(event.partner_id)
        writer.writerow(["Partner name", partner.name if partner else ""])
        writer.writerow(["Partner EBU", partner.ebu_number if partner else ""])
        writer.writerow([])

        # -----------------------
        # BOARD HEADER
        # -----------------------

        writer.writerow(
            [
                "Board",
                "Contract",
                "Declarer",
                "Lead",
                "Tricks",
                "Score",
                "Vulnerable",
                "Orientation",
                "Opponents",
                "Section",
                "Team Score",
                "IMPs",
                "Notes",
            ]
        )

        # -----------------------
        # BOARDS
        # -----------------------

        for board in event.boards or []:
            writer.writerow(
                [
                    board.board_number,
                    board.contract,
                    board.declarer,
                    board.lead,
                    board.tricks,
                    board.score,
                    board.vulnerable,
                    board.orientation,
                    board.opponents,
                    board.section,
                    board.team_score,
                    board.imps,
                    board.notes or "",
                ]
            )

    share_file_email(filepath, "Event")
    return filepath


def get_export_dir():
    # This is accessible via plain adb pull without run-as
    export_dir = Path("/sdcard/Download/scorecard")
    export_dir.mkdir(parents=True, exist_ok=True)
    return export_dir


def share_file_email(filepath: str, file_type: str = "") -> None:
    settings = App.get_running_app().settings
    email_address = settings.email_address if settings else ""
    try:
        from jnius import autoclass, cast

        kivy_python = autoclass("org.kivy.android.PythonActivity")
        kivy_intent = autoclass("android.content.Intent")
        # CharSequence = autoclass("java.lang.CharSequence")
        java_string = autoclass("java.lang.String")

        intent = kivy_intent(kivy_intent.ACTION_SEND)
        intent.setType("text/plain")
        intent.putExtra(
            kivy_intent.EXTRA_SUBJECT,
            java_string(f"Score Card Export - {file_type}"),
        )

        with open(filepath) as f:
            content = f.read()

        intent.putExtra(kivy_intent.EXTRA_TEXT, java_string(content))
        intent.putExtra(kivy_intent.EXTRA_EMAIL, [email_address])

        activity = kivy_python.mActivity
        title = cast("java.lang.CharSequence", java_string("Share"))
        chooser = kivy_intent.createChooser(intent, title)
        activity.startActivity(chooser)
    except ImportError:
        msg_dialog(
            "Export Complete", f"File would be emailed to {email_address}"
        )
    except Exception as e:
        logging.error(f">>> share failed: {e}")
        logging.error(traceback.format_exc())
        print(e)
        msg_dialog("Export Failed", f"Failed to share file: {e}")


def export_partners_csv(partners: list) -> str:
    """Export partners to CSV. Returns the file path."""
    downloads = _get_download_dir()
    filename = "partners.csv"
    filepath = downloads / filename

    fieldnames = [
        "Name",
        "EBU Number",
    ]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for partner in partners or []:
            writer.writerow(
                {
                    "Name": partner.name,
                    "EBU Number": partner.ebu_number,
                }
            )

    share_file_email(filepath, "Partners")
    return str(filepath)


def _get_download_dir() -> Path:
    # On Android write to app storage, on desktop write to ~/Downloads
    if platform == "android":
        from android.storage import app_storage_path

        downloads = Path(app_storage_path()) / "Download"
    else:
        downloads = Path.home() / "Downloads"

    downloads.mkdir(parents=True, exist_ok=True)
    return downloads
