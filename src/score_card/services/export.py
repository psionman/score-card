# services/export.py
import csv
import logging
import traceback
from pathlib import Path

from kivy.app import App
from kivy.utils import platform
from models.event import Event
from services.board import BoardService
from utilities import msg_dialog


def export_event_csv(event: Event) -> str:
    """Export event boards to CSV. Returns the file path."""
    downloads = _get_download_dir()
    safe_name = event.name.replace(" ", "_").replace("/", "-")
    filename = f"{event.date}_{safe_name}.csv"
    filepath = downloads / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
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
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        event.boards = BoardService.get_boards_for_event(event.id)

        for board in event.boards or []:
            writer.writerow(
                {
                    "Board": board.board_number,
                    "Contract": board.contract,
                    "Declarer": board.declarer,
                    "Lead": board.lead,
                    "Tricks": board.tricks,
                    "Score": board.score,
                    "Vulnerable": board.vulnerable,
                    "Orientation": board.orientation,
                    "Opponents": board.opponents,
                    "Section": board.section,
                    "Team Score": board.team_score,
                    "IMPs": board.imps,
                    "Notes": board.notes or "",
                }
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

        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        Intent = autoclass("android.content.Intent")
        CharSequence = autoclass("java.lang.CharSequence")
        String = autoclass("java.lang.String")

        intent = Intent(Intent.ACTION_SEND)
        intent.setType("text/plain")
        intent.putExtra(
            Intent.EXTRA_SUBJECT, String(f"Score Card Export - {file_type}")
        )

        with open(filepath) as f:
            content = f.read()

        intent.putExtra(Intent.EXTRA_TEXT, String(content))
        intent.putExtra(Intent.EXTRA_EMAIL, [email_address])

        activity = PythonActivity.mActivity
        title = cast("java.lang.CharSequence", String("Share"))
        chooser = Intent.createChooser(intent, title)
        activity.startActivity(chooser)
    except ImportError:
        msg_dialog(
            "Export Complete", f"File would be emailed to {email_address}"
        )
    except Exception as e:
        logging.error(f">>> share failed: {e}")
        logging.error(traceback.format_exc())
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
