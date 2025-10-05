import os
import sys
import re
import glob
import csv
import sqlite3
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QScrollArea, QWidget, QHBoxLayout, QSizePolicy
)
from PySide6.QtCore import Qt
from Save.save import init_new_db

from League.game import Game 
from League.linked_list import LinkedList 
from League.player import Player, Pitcher 
from League.team import Team


# Map table names to their primary key
PRIMARY_KEYS = {
    "team": "teamID",
    "player": "playerID",
    "pitcher": "playerID",
    "league": "leagueID"
}

ALLOWED_TABLES = {"league", "team", "player", "pitcher"}


# ----------------------- Dialogs -----------------------
class SessionChoiceDialog(QDialog):
    """Dialog to select a CSV session."""

    def __init__(self, sessions: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select CSV Import Session")
        self.choice = None
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        self.setSizeGripEnabled(True)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        title_label = QLabel("Multiple CSV save sessions found.\nSelect one to import:")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setWordWrap(True)
        main_layout.addWidget(title_label)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(10)

        for session in sorted(sessions.keys()):
            btn = QPushButton(f"Session {session} ({len(sessions[session])} files)")
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setMinimumHeight(40)
            btn.clicked.connect(lambda checked=False, s=session: self.choose(s))
            scroll_layout.addWidget(btn)

        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll, stretch=1)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumHeight(35)
        cancel_btn.clicked.connect(self.reject)
        main_layout.addWidget(cancel_btn, alignment=Qt.AlignCenter)

    def choose(self, session: str):
        self.choice = session
        self.accept()


class DatabaseChoiceDialog(QDialog):
    """Dialog to choose new DB or update existing."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Database Choice")
        self.choice = None
        self.setMinimumWidth(400)
        self.setSizeGripEnabled(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        layout.addWidget(QLabel(
            "Do you want to create a new database or update an existing one?"
        ))

        button_layout = QHBoxLayout()
        new_db_btn = QPushButton("Create New Database")
        update_btn = QPushButton("Update Existing Database")
        cancel_btn = QPushButton("Cancel")

        new_db_btn.setMinimumHeight(40)
        update_btn.setMinimumHeight(40)
        cancel_btn.setMinimumHeight(40)

        new_db_btn.clicked.connect(self.choose_new_db)
        update_btn.clicked.connect(self.choose_update)
        cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(new_db_btn)
        button_layout.addWidget(update_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

    def choose_new_db(self):
        self.choice = "new database"
        self.accept()

    def choose_update(self):
        self.choice = "update existing"
        self.accept()


class OverwriteDialog(QDialog):
    """Dialog to choose overwrite, skip, or cancel when updating DB."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("CSV Import Confirmation")
        self.choice = "cancel"
        self.setMinimumWidth(400)
        self.setSizeGripEnabled(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        layout.addWidget(QLabel(
            "Do you want to overwrite existing data in ALL database tables?\n\n"
            "Yes = Overwrite/Update existing rows\n"
            "No = Skip rows that already exist\n"
            "Cancel = Cancel all CSV imports"
        ))

        button_layout = QHBoxLayout()
        yes_btn = QPushButton("Yes")
        no_btn = QPushButton("No")
        cancel_btn = QPushButton("Cancel")

        yes_btn.setMinimumHeight(40)
        no_btn.setMinimumHeight(40)
        cancel_btn.setMinimumHeight(40)

        yes_btn.clicked.connect(self.choose_overwrite)
        no_btn.clicked.connect(self.choose_skip)
        cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(yes_btn)
        button_layout.addWidget(no_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

    def choose_overwrite(self):
        self.choice = "overwrite"
        self.accept()

    def choose_skip(self):
        self.choice = "skip"
        self.accept()


class SummaryDialog(QDialog):
    """Dialog to show CSV import summary."""

    def __init__(self, summary: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("CSV Import Summary")
        self.setMinimumWidth(400)
        self.setSizeGripEnabled(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        total_inserted = sum(v["inserted"] for v in summary.values())
        total_skipped = sum(v["skipped"] for v in summary.values())
        total_overwritten = sum(v["overwritten"] for v in summary.values())

        layout.addWidget(QLabel("<b>CSV Import Results:</b>"))

        for table, stats in summary.items():
            if stats.get("error", False):
                layout.addWidget(QLabel(f"⚠️ {table}: Skipped (table missing or no matching columns)"))
            else:
                layout.addWidget(QLabel(
                    f"✅ {table}: {stats['inserted']} inserted, "
                    f"{stats['skipped']} skipped, "
                    f"{stats['overwritten']} overwritten"
                ))

        layout.addWidget(QLabel("<hr>"))
        layout.addWidget(QLabel(
            f"<b>Total:</b> {total_inserted} inserted, "
            f"{total_skipped} skipped, "
            f"{total_overwritten} overwritten"
        ))

        ok_btn = QPushButton("OK")
        ok_btn.setMinimumHeight(35)
        ok_btn.clicked.connect(self.accept)
        layout.addWidget(ok_btn, alignment=Qt.AlignCenter)


# ----------------------- CSV Loader Utilities -----------------------
def get_csv_files(directory: str) -> list:
    return glob.glob(os.path.join(directory, "*.csv"))


def group_csv_by_session(csv_files: list) -> dict:
    """Group CSV files by session timestamp, ignore sqlite_sequence."""
    session_pattern = re.compile(
        r"^(league|team|player|pitcher)_([0-9]+(?:\([0-9]+\))?)\.csv$", re.IGNORECASE
    )
    sessions = {}
    for f in csv_files:
        filename = os.path.basename(f)
        if filename.startswith("sqlite_sequence"):
            continue
        match = session_pattern.match(filename)
        if match:
            table, session = match.groups()
            table = table.lower()
            if table in ALLOWED_TABLES:
                sessions.setdefault(session, []).append((table, f))
    return sessions


def insert_csv_to_table(table: str, csv_path: str, conn: sqlite3.Connection, mode: str, summary: dict):
    """Insert CSV into SQLite table according to overwrite/skip mode."""
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table})")
    table_columns = [info[1] for info in cursor.fetchall()]
    if not table_columns:
        summary[table] = {"inserted": 0, "skipped": 0, "overwritten": 0, "error": True}
        return

    primary_key = PRIMARY_KEYS.get(table)
    inserted = skipped = overwritten = 0

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        valid_columns = [col for col in reader.fieldnames if col in table_columns]
        placeholders = ", ".join(["?"] * len(valid_columns))
        for row in reader:
            values = [row.get(col, None) for col in valid_columns]
            table_hint = row.keys()
            print("csv values: ", values)
            print("row in reader-fields: ", row)
            print("table hint - instance type: ", table_hint)
            if mode == "overwrite":
                cursor.execute(f"INSERT OR REPLACE INTO {table} ({', '.join(valid_columns)}) VALUES ({placeholders})", values)

                load_all_to_gui(table_hint, values)
                
                
                overwritten += 1
            elif mode == "skip":
                if primary_key and primary_key in valid_columns:
                    pk_value = row.get(primary_key)
                    cursor.execute(f"SELECT 1 FROM {table} WHERE {primary_key} = ?", (pk_value,))
                    if cursor.fetchone():
                        skipped += 1
                        continue
                cursor.execute(f"INSERT INTO {table} ({', '.join(valid_columns)}) VALUES ({placeholders})", values)
                inserted += 1
    conn.commit()
    summary[table] = {"inserted": inserted, "skipped": skipped, "overwritten": overwritten, "error": False}


# ----------------------- Full CSV Loader -----------------------
def load_all_csv_to_db(league, directory: str, db_path: str, parent=None):
    """
    Full workflow: session selection + database choice + overwrite choice + import + summary.
    """
    
    csv_files = get_csv_files(directory)
    sessions = group_csv_by_session(csv_files)
    if not sessions:
        print("⚠️ No valid CSV session files found in directory.")
        return

    # Step 1: Session choice
    if len(sessions) > 1:
        session_dialog = SessionChoiceDialog(sessions, parent=parent)
        session_dialog.exec()
        chosen_session = session_dialog.choice
        if not chosen_session:
            print("⏹️ CSV import cancelled: no session selected")
            return
    else:
        chosen_session = list(sessions.keys())[0]

    selected_files = sessions[chosen_session]

    # Step 2: Database choice
    db_dialog = DatabaseChoiceDialog(parent=parent)
    db_dialog.exec()
    db_choice = db_dialog.choice
    if not db_choice:
        print("⏹️ CSV import cancelled: no database choice")
        return

    if db_choice == "new database":
        print("Creating new database...")
        # Handle DB creation logic separately if needed
        # delete League.db 
        # db exists 
        try: 
            conn = sqlite3.connect(db_path)
            conn.close() 
        except Exception as e: 
            print(f"Error closing connection: {e}")
            return 
        
        if os.path.exists(db_path):
            try:
                os.remove(db_path)
                print(f"Database file '{db_path}' deleted successfully.")
                init_new_db(db_path, league)
            except OSError as e:
                print(f"Error deleting database file '{db_path}': {e}") 
        else:
            print(f"No DB found at {db_path}!") 

        mode = "overwrite"  # assume new DB → overwrite
    else:
        # Step 3: Overwrite/skip/cancel choice
        overwrite_dialog = OverwriteDialog(parent=parent)
        overwrite_dialog.exec()
        mode = overwrite_dialog.choice
        if mode == "cancel":
            print("⏹️ CSV import cancelled by user")
            return

    # Step 4: Insert CSVs
    conn = sqlite3.connect(db_path)
    summary = {}
    try:
        for table, filepath in selected_files:
            insert_csv_to_table(table, filepath, conn, mode, summary)
    finally:
        conn.close()

    # Step 5: Show summary
    summary_dialog = SummaryDialog(summary, parent=parent)
    summary_dialog.exec()

def load_all_to_gui(attrs, vals):
    lst_attr = [x for x in attrs]
    lst_vals = [x for x in vals]
    print("instance type: ", lst_attr[0])
    print("attrs for gui: ", lst_attr)
    print("vals for gui: ", lst_vals)


if __name__ == "__main__":
   app = QApplication(sys.argv)
   load_all_csv_to_db("Saved/CSV", "Saved/DB/League.db")
   

   sys.exit(app.exec())
