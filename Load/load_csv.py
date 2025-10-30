import os
import sys
import re
import glob
import csv
import sqlite3
import json
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QScrollArea, QWidget, QHBoxLayout, QSizePolicy
)
from PySide6.QtCore import Qt
from Save.save import init_new_db
from League.stack import InstanceStack
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
    # Search recursively to include session subfolders like CSV/save_1/*.csv
    return glob.glob(os.path.join(directory, "**", "*.csv"), recursive=True)


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


def insert_csv_to_table(table: str, csv_path: str, conn: sqlite3.Connection, mode: str, summary: dict, stack: InstanceStack, parent, league: LinkedList):
    """Insert CSV into SQLite table according to overwrite/skip mode."""
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table})")
    table_columns = [info[1] for info in cursor.fetchall()]
    # use the provided league instance so teams/players accumulate across tables

    print('table cols: ', table_columns)

    if not table_columns:
        summary[table] = {"inserted": 0, "skipped": 0, "overwritten": 0, "error": True}
        return

    primary_key = PRIMARY_KEYS.get(table)
    inserted = skipped = overwritten = 0

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        valid_columns = [col for col in reader.fieldnames if col in table_columns]
        placeholders = ", ".join(["?"] * len(valid_columns))

        print('valid cols: ', valid_columns)

        for row in reader:
            values = [row.get(col, None) for col in valid_columns]
            
            print("csv values: ", values)
            #print("row in reader-fields: ", row)
            #print("table hint - instance type: ", table_hint)
            
            if mode == "overwrite":
                # Check if row exists to distinguish insert vs replace
                existed = False
                if primary_key and primary_key in valid_columns:
                    pk_value = row.get(primary_key)
                    cursor.execute(f"SELECT 1 FROM {table} WHERE {primary_key} = ?", (pk_value,))
                    existed = cursor.fetchone() is not None
                
                cursor.execute(f"INSERT OR REPLACE INTO {table} ({', '.join(valid_columns)}) VALUES ({placeholders})", values)

                if existed:
                    overwritten += 1
                else:
                    inserted += 1

                # collect ordered row aligned to valid_columns and annotate table
                ordered = {col: row.get(col, None) for col in valid_columns}
                stack.add(table, ordered, values)

            elif mode == "skip":
                if primary_key and primary_key in valid_columns:
                    pk_value = row.get(primary_key)
                    cursor.execute(f"SELECT 1 FROM {table} WHERE {primary_key} = ?", (pk_value,))
                    if cursor.fetchone():
                        skipped += 1
                        continue
                cursor.execute(f"INSERT INTO {table} ({', '.join(valid_columns)}) VALUES ({placeholders})", values)
                inserted += 1

                # collect ordered row aligned to valid_columns and annotate table
                ordered = {col: row.get(col, None) for col in valid_columns}
                stack.add(table, ordered, values)

    conn.commit()
    summary[table] = {"inserted": inserted, "skipped": skipped, "overwritten": overwritten, "error": False}
    
    
    # Defer building GUI until all tables are processed. Instances
    # will be collected across calls via the shared InstanceStack.

def load_all_gui(instances, parent, league):
    # Process in deterministic order: league -> team -> player -> pitcher
    league_items = []
    team_items = []
    player_items = []
    pitcher_items = []

    for item in instances:
        key = list(item.keys()).pop()
        if key == 'league':
            league_items.append(item)
        elif key == 'team':
            team_items.append(item)
        elif key == 'player':
            player_items.append(item)
        elif key == 'pitcher':
            pitcher_items.append(item)

    # League
    for item in league_items:
        vals = list(item.values()).pop()
        for el in vals:
            attr = el[0]
            val = el[1]
            if val == '__SQL_NULL__':
                continue
            load_league_gui(attr, val, league)

    # Teams
    for item in team_items:
        vals = list(item.values()).pop()
        team = Team(league, 'team', 'manager')
        for el in vals:
            attr = el[0]
            val = el[1]
            if attr in ('players',):
                continue
            elif attr in ('lineup', 'positions'):
                # parse JSON if string
                try:
                    parsed = json.loads(val) if isinstance(val, str) else val
                except Exception:
                    parsed = val
                load_team_gui(attr, parsed, team)
            elif attr == 'logo':
                # Keep logo as string path - GUI will convert to QIcon when displaying
                if val and val not in (0, '0', 0.0, '0.0', ''):
                    load_team_gui(attr, val, team)
                else:
                    team.logo = None
            elif attr in ('teamID', 'leagueID'):
                # normalize numeric ids (handle '01', '1 ', '1.0')
                def _normalize_id_local(v):
                    try:
                        return int(v)
                    except Exception:
                        pass
                    try:
                        s = str(v).strip().strip('"').strip("'")
                        if '.' in s:
                            f = float(s)
                            if f.is_integer():
                                return int(f)
                        if s.isdigit():
                            return int(s)
                        return s
                    except Exception:
                        return v
                norm = _normalize_id_local(val)
                load_team_gui(attr, norm, team)
            else:
                if val in (0, '0', 0.0, '0.0'):
                    continue
                load_team_gui(attr, val, team)
        league.add_team(team)
    print('league after load', league)
    print('league after load', league.view_all())
    print(f'LinkedList.COUNT (class var): {LinkedList.COUNT}')
    print(f'league.COUNT (checking if instance var exists): {getattr(league, "COUNT", "No instance var - using class var")}')

    # Build quick-lookup maps for teams
    def _norm_name(s):
        try:
            return str(s).strip().lower()
        except Exception:
            return s
    team_name_map = { _norm_name(t.name): t for t in league.get_all_objs() }
    team_id_map = { str(getattr(t, 'teamID', '')).strip(): t for t in league.get_all_objs() }

    # Helper: normalize ids from CSV and robust team resolve by ID or name
    def _normalize_id(v):
        if v is None:
            return None
        try:
            return int(v)
        except Exception:
            pass
        try:
            s = str(v).strip().strip('"').strip("'")
            if '.' in s:
                f = float(s)
                if f.is_integer():
                    return int(f)
            # JSON numeric
            try:
                j = json.loads(s)
                if isinstance(j, (int, float)):
                    jf = float(j)
                    return int(jf) if jf.is_integer() else s
            except Exception:
                pass
            if s.isdigit():
                return int(s)
            return s
        except Exception:
            return v

    def _resolve_team_by_id_or_name(id_val, name_val):
        # Try by ID first
        if id_val is not None:
            norm_id = _normalize_id(id_val)
            if isinstance(norm_id, int):
                found = league.find_teamID(norm_id)
                if found is not None:
                    return found
            # fallback: compare as strings
            try:
                target = str(norm_id if norm_id is not None else id_val).strip()
                if target in team_id_map:
                    return team_id_map[target]
            except Exception:
                pass
        # Try by name next
        if name_val:
            try:
                by_map = team_name_map.get(_norm_name(name_val))
                if by_map:
                    return by_map
                return league.find_team(name_val)
            except Exception:
                return None
        return None

    # Players
    for item in player_items:
        vals = list(item.values()).pop()
        # Temporary minimal team placeholder; will reassign to real team
        team_sample = Team(league, "team sample", "manager")
        player = Player('player', 0, team_sample, league)
        find_team = None
        fallback_team_name = None
        captured_player_id = None
        pending_team_id = None
        parsed_positions = []
        for el in vals:
            attr = el[0]
            val = el[1]
            if attr == 'positions':
                # parse positions JSON
                try:
                    parsed = json.loads(val) if isinstance(val, str) else val
                except Exception:
                    parsed = val
                load_player_gui(attr, parsed, player)
                try:
                    parsed_positions = list(parsed)
                except Exception:
                    parsed_positions = []
            elif attr == 'teamID':
                # store as int if possible
                try:
                    pending_team_id = int(val)
                except Exception:
                    pending_team_id = val
                # also set attribute with normalized int
                try:
                    load_player_gui(attr, int(val), player)
                except Exception:
                    load_player_gui(attr, val, player)
            elif attr == 'playerID':
                try:
                    captured_player_id = int(val)
                    load_player_gui(attr, captured_player_id, player)
                except Exception:
                    captured_player_id = val
                    load_player_gui(attr, val, player)
            elif attr == 'team':
                fallback_team_name = val
                # DON'T set player.team to the string - we'll set it later after resolving the Team object
            elif attr == 'image':
                # Keep image as string path for player - stat dialog handles conversion
                # Don't convert to QIcon here, just store the path
                if val and val not in (0, '0', 0.0, '0.0', ''):
                    player.image = val
                else:
                    player.image = None
            else:
                if val in (0, '0', 0.0, '0.0'):
                    continue
                load_player_gui(attr, val, player)
        # resolve team after reading all attrs: by name first per requirement, then by ID
        if fallback_team_name:
            try:
                # prefer map for case-insensitive/trim matches
                find_team = team_name_map.get(_norm_name(fallback_team_name)) or league.find_team(fallback_team_name)
            except Exception:
                find_team = None
        if find_team is None and pending_team_id is not None:
            find_team = _resolve_team_by_id_or_name(pending_team_id, None)
        
        # Validate and set team FIRST, before any type conversions
        if find_team is not None:
            # Validate that find_team is actually a Team object, not a string
            if isinstance(find_team, str):
                print(f"ERROR: find_team is a string '{find_team}' instead of a Team object for player {getattr(player, 'name', 'unknown')}")
                print(f"  fallback_team_name: {fallback_team_name}")
                print(f"  pending_team_id: {pending_team_id}")
                find_team = None  # Set to None so it's handled below
            
            if find_team is not None:
                # Set team references on player first
                player.team = find_team
                player.teamID = find_team.teamID
                player.league = league
                player.leagueID = league.leagueID
                
                # NOW convert to Pitcher if needed (after team is set properly)
                if 'pitcher' in parsed_positions:
                    temp = player
                    pitcher_player = Pitcher(temp.name, temp.number, temp.team, temp.league, positions=parsed_positions)
                    # copy offense stats and ids
                    for k in ['pa','at_bat','fielder_choice','hit','bb','hbp','put_out','so','hr','rbi','runs','singles','doubles','triples','sac_fly','OBP','BABIP','SLG','AVG','ISO','image','playerID','leagueID','teamID']:
                        setattr(pitcher_player, k, getattr(temp, k, getattr(pitcher_player, k, 0)))
                    player = pitcher_player
            else:
                print(f"Warning: team not found for player {getattr(player, 'name', '')} (after validation)")
                continue  # Skip this player
            exists = False
            pid = getattr(player, 'playerID', None)
            for existing in find_team.players:
                if pid is not None and getattr(existing, 'playerID', None) == pid:
                    exists = True
                    break
                if pid is None and existing.name == player.name:
                    exists = True
                    break
            if not exists:
                find_team.add_player(player)
        else:
            print(f"Warning: team not found for player {getattr(player, 'name', '')} (teamID/team name mismatch)")

    # Pitchers
    for item in pitcher_items:
        vals = list(item.values()).pop()
        # Create a temporary placeholder team object to initialize the pitcher
        temp_team = Team(league, 'placeholder', 'manager')
        pitcher = Pitcher('pitcher', 0, temp_team, league)
        find_team = None
        fallback_team_name = None
        captured_player_id = None
        pending_team_id = None
        for el in vals:
            attr = el[0]
            val = el[1]
            if attr == 'teamID':
                try:
                    pending_team_id = int(val)
                    load_player_gui(attr, pending_team_id, pitcher)
                except Exception:
                    pending_team_id = val
                    load_player_gui(attr, val, pitcher)
            elif attr == 'playerID':
                try:
                    captured_player_id = int(val)
                except Exception:
                    captured_player_id = val
                load_player_gui(attr, captured_player_id, pitcher)
            elif attr == 'team':
                fallback_team_name = val
                # DON'T set pitcher.team to the string - we'll set it later after resolving the Team object
            elif attr == 'image':
                # Keep image as string path for pitcher - stat dialog handles conversion
                if val and val not in (0, '0', 0.0, '0.0', ''):
                    pitcher.image = val
                else:
                    pitcher.image = None
            else:
                if val in (0, '0', 0.0, '0.0'):
                    continue 
                load_pitcher_gui(attr, val, pitcher)
        # resolve team after reading all attrs: by name first per requirement, then by ID
        if fallback_team_name:
            try:
                find_team = team_name_map.get(_norm_name(fallback_team_name)) or league.find_team(fallback_team_name)
            except Exception:
                find_team = None
        if find_team is None and pending_team_id is not None:
            find_team = _resolve_team_by_id_or_name(pending_team_id, None)
        
        # Validate that find_team is actually a Team object, not a string
        if find_team is not None and isinstance(find_team, str):
            print(f"ERROR: find_team is a string '{find_team}' instead of a Team object for pitcher {getattr(pitcher, 'name', 'unknown')}")
            print(f"  fallback_team_name: {fallback_team_name}")
            print(f"  pending_team_id: {pending_team_id}")
            find_team = None
        
        if find_team is not None:
            # If a matching player already exists, upgrade/merge
            existing_index = None
            existing_player = None
            if captured_player_id is not None:
                for idx, p in enumerate(find_team.players):
                    if getattr(p, 'playerID', None) == captured_player_id:
                        existing_index = idx
                        existing_player = p
                        break
            if existing_player is not None:
                # Preserve offense stats and identity, replace with Pitcher subtype if needed
                if not isinstance(existing_player, Pitcher):
                    new_pitcher = Pitcher(existing_player.name, existing_player.number, find_team, league, positions=existing_player.positions)
                    # copy offensive stats
                    for k in ['pa','at_bat','fielder_choice','hit','bb','hbp','put_out','so','hr','rbi','runs','singles','doubles','triples','sac_fly','OBP','BABIP','SLG','AVG','ISO','image','playerID','leagueID','teamID']:
                        setattr(new_pitcher, k, getattr(existing_player, k, getattr(new_pitcher, k, 0)))
                    # merge pitcher stats from current pitcher instance
                    for k in ['wins','losses','era','games_played','games_started','games_completed','shutouts','saves','save_ops','ip','p_at_bats','p_hits','p_runs','er','p_hr','p_hb','p_bb','p_so','WHIP','p_avg','k_9','bb_9']:
                        setattr(new_pitcher, k, getattr(pitcher, k, getattr(new_pitcher, k, 0)))
                    # ensure positions includes pitcher
                    try:
                        if 'pitcher' not in new_pitcher.positions:
                            new_pitcher.positions.append('pitcher')
                    except Exception:
                        pass
                    find_team.players[existing_index] = new_pitcher
                else:
                    # Already a Pitcher; just update pitching stats
                    for k in ['wins','losses','era','games_played','games_started','games_completed','shutouts','saves','save_ops','ip','p_at_bats','p_hits','p_runs','er','p_hr','p_hb','p_bb','p_so','WHIP','p_avg','k_9','bb_9']:
                        setattr(existing_player, k, getattr(pitcher, k, getattr(existing_player, k, 0)))
            else:
                # No existing player, attach pitcher
                pitcher.team = find_team
                pitcher.teamID = find_team.teamID
                pitcher.league = league
                pitcher.leagueID = league.leagueID
                try:
                    if 'pitcher' not in pitcher.positions:
                        pitcher.positions.append('pitcher')
                except Exception:
                    pass
                # avoid duplicate by name+playerID
                dup = False
                for existing in find_team.players:
                    if getattr(existing, 'playerID', None) == getattr(pitcher, 'playerID', None):
                        dup = True
                        break
                    if existing.name == pitcher.name and 'pitcher' in getattr(existing, 'positions', []):
                        dup = True
                        break
                if not dup:
                    find_team.add_player(pitcher)
        else:
            print(f"Warning: team not found for pitcher {getattr(pitcher, 'name', '')} (teamID/team name mismatch)")

    # assign Main Window - league - inherited by all - with CSV load
    setattr(parent, 'league', league)
    
    # Update league references in all child views to ensure they use the new league object
    if parent:
        try:
            if hasattr(parent, 'league_view_players'):
                parent.league_view_players.league = league
                print("Updated league_view_players league reference")
            if hasattr(parent, 'league_view_teams'):
                parent.league_view_teams.league = league
                print("Updated league_view_teams league reference")
            if hasattr(parent, 'leaderboard'):
                parent.leaderboard.league = league
                print("Updated leaderboard league reference")
            if hasattr(parent, 'refresh'):
                parent.refresh.league = league
                print("Updated refresh league reference")
        except Exception as e:
            print(f"Warning: Could not update all league references: {e}")

    # call refresh tree widget views after Main Window league updated
    try:
        if hasattr(parent, 'refresh_view') and callable(parent.refresh_view):
            parent.refresh_view()
    except Exception as e:
        print(f"Refresh note: {e}")
        
def load_league_gui(attr, val, league):
    setattr(league, attr, val)

def load_team_gui(attr, val, team):
    setattr(team, attr, val)

def load_player_gui(attr, val, player):
    setattr(player, attr, val) 

def load_pitcher_gui(attr, val, pitcher):
    setattr(pitcher, attr, val)

# ----------------------- Full CSV Loader -----------------------
def load_all_csv_to_db(league, directory: str, db_path: str, stack, parent=None):
    """
    Full workflow: session selection + database choice + overwrite choice + import + summary.
    """
    
    # Check if league already has data (teams/players in memory)
    if LinkedList.COUNT > 0:
        from PySide6.QtWidgets import QMessageBox
        reply = QMessageBox.question(
            parent,
            "League Data Exists",
            f"The league already has {LinkedList.COUNT} team(s) loaded.\n\n"
            "Loading new data will replace all current data in memory.\n\n"
            "Do you want to continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.No:
            print("Load cancelled - user chose to keep existing league data")
            return
    
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
        # Step 2a: Close any existing connections to the database
        try: 
            conn = sqlite3.connect(db_path)
            conn.close() 
        except Exception as e: 
            print(f"Warning: Could not connect to close existing connection: {e}")
        
        # Step 2b: Delete the existing database file to drop all data
        if os.path.exists(db_path):
            try:
                os.remove(db_path)
                print(f"Database file '{db_path}' deleted successfully.")
            except OSError as e:
                print(f"Error: Failed to delete database file '{db_path}': {e}")
                print("Cannot create new database without deleting the old one. Aborting.")
                return
        
        # Step 2c: Clear the league object in memory to remove all existing data
        print("Clearing league data from memory...")
        # Clear all teams from league
        league.head = None
        # Reset the CLASS variable COUNT (not an instance variable)
        LinkedList.COUNT = 0
        # Remove any instance variable COUNT if it exists
        if hasattr(league, 'COUNT') and 'COUNT' in league.__dict__:
            delattr(league, 'COUNT')
        
        print(f"League data cleared. LinkedList.COUNT reset to: {LinkedList.COUNT}")
        print(f"league has instance COUNT: {'COUNT' in league.__dict__}")
        print("Only CSV data will be loaded.")
        
        # Clear all GUI tree widgets to remove visual display of old data
        if parent and hasattr(parent, 'league_view_players'):
            print("Clearing GUI tree widgets...")
            try:
                # Clear player views
                if hasattr(parent.league_view_players, 'tree1_top'):
                    parent.league_view_players.tree1_top.clear()
                if hasattr(parent.league_view_players, 'tree2_top'):
                    parent.league_view_players.tree2_top.clear()
                
                # Clear team views
                if hasattr(parent, 'league_view_teams'):
                    if hasattr(parent.league_view_teams, 'tree1_bottom'):
                        parent.league_view_teams.tree1_bottom.clear()
                    if hasattr(parent.league_view_teams, 'tree2_bottom'):
                        parent.league_view_teams.tree2_bottom.clear()
                
                # Clear leaderboard
                if hasattr(parent, 'leaderboard') and hasattr(parent.leaderboard, 'tree_widget'):
                    parent.leaderboard.tree_widget.clear()
                    
                print("GUI cleared successfully.")
            except Exception as e:
                print(f"Warning: Could not clear all GUI elements: {e}")
        
        print("League data cleared. Only CSV data will be loaded.")
        
        # Step 2d: Create fresh database with empty tables
        try:
            init_new_db(db_path, league)
            print("New database initialized with empty tables.")
        except Exception as e:
            print(f"Error: Failed to initialize new database: {e}")
            return

        mode = "overwrite"  # New DB is empty, so all inserts will be new
    else:
        # Step 3: Overwrite/skip/cancel choice
        overwrite_dialog = OverwriteDialog(parent=parent)
        overwrite_dialog.exec()
        mode = overwrite_dialog.choice
        if mode == "cancel":
            print("⏹️ CSV import cancelled by user")
            return

    # Step 4: Insert CSVs (collect to local instance stack regardless of caller)
    conn = sqlite3.connect(db_path)
    summary = {}
    local_stack = InstanceStack()
    try:
        for table, filepath in selected_files:
            insert_csv_to_table(table, filepath, conn, mode, summary, local_stack, parent, league)
    finally:
        conn.close()

    # Step 4b: After all tables processed, build GUI once
    try:
        instances = local_stack.getInstances()
        if instances:
            load_all_gui(instances, parent, league)
    except Exception as e:
        import traceback
        print(f"Build GUI after CSV import failed: {e}")
        print(f"Full traceback:\n{traceback.format_exc()}")

    # Step 5: Show summary
    summary_dialog = SummaryDialog(summary, parent=parent)
    summary_dialog.exec()



if __name__ == "__main__":
   app = QApplication(sys.argv)
   load_all_csv_to_db("Saved/CSV", "Saved/DB/League.db")
   

   sys.exit(app.exec())
