# services/export.py
import csv
import os
from pathlib import Path
from models.event import Event
from kivy.utils import platform


def export_event_csv(event: Event) -> str:
    """Export event boards to CSV. Returns the file path."""
    downloads = _get_download_dir()
    safe_name = event.name.replace(" ", "_").replace("/", "-")
    filename = f"{event.date}_{safe_name}.csv"
    filepath = downloads / filename

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

        for board in (event.boards or []):
            writer.writerow({
                "Board":       board.board_number,
                "Contract":    board.contract,
                "Declarer":    board.declarer,
                "Lead":        board.lead,
                "Tricks":      board.tricks,
                "Score":       board.score,
                "Vulnerable":  board.vulnerable,
                "Orientation": board.orientation,
                "Opponents":   board.opponents,
                "Section":     board.section,
                "Team Score":  board.team_score,
                "IMPs":        board.imps,
                "Notes":       board.notes or "",
            })

    return filepath


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

        for partner in (partners or []):
            writer.writerow({
                "Name":       partner.name,
                "EBU Number":    partner.ebu_number,
            })

    return filepath


def _get_download_dir() -> Path:
    # On Android write to app storage, on desktop write to ~/Downloads
    if platform == "android":
        from android.storage import app_storage_path
        downloads = Path(app_storage_path()) / "Download"
    else:
        downloads = Path.home() / "Downloads"

    downloads.mkdir(parents=True, exist_ok=True)
    return downloads
