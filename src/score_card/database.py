# database.py

import sqlite3
import os
import shutil
from pathlib import Path
from kivy.app import App

def get_db_path():
    app = App.get_running_app()

    if app is None:
        # fallback for desktop / early import
        return Path(".") / "events.db"

    return Path(app.user_data_dir) / "events.db"


def get_connection():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # -----------------------
    # PARTNERS
    # -----------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS partners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            ebu_number TEXT NOT NULL
        );
    """)

    # -----------------------
    # EVENTS
    # -----------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,

            partner_id INTEGER NOT NULL,

            location TEXT,
            notes TEXT,

            created_at TEXT DEFAULT (datetime('now')),

            FOREIGN KEY(partner_id) REFERENCES partners(id)
        );
    """)

    # -----------------------
    # BOARDS
    # -----------------------
    # cur.execute("""
    #     DROP TABLE IF EXISTS boards;
    # """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS boards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,

            board_number INTEGER NOT NULL,

            vulnerable TEXT,
            orientation TEXT NOT NULL,

            opponents INTEGER NOT NULL,

            contract TEXT NOT NULL,
            declarer TEXT NOT NULL,
            lead TEXT NOT NULL,

            tricks INTEGER NOT NULL,

            score INTEGER NOT NULL,

            section TEXT,
            team_score INTEGER,
            imps INTEGER,
            notes TEXT,

            FOREIGN KEY(event_id) REFERENCES events(id)
        );
    """)

    conn.commit()
    conn.close()
