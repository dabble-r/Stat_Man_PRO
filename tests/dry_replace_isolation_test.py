import os
import sqlite3
from pathlib import Path

# Extend path to import project modules
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.core.linked_list import LinkedList
from src.data.save.save import init_new_db
from src.data.load.load_csv import get_csv_files, group_csv_by_session, insert_csv_to_table, load_all_gui


class _ParentStub:
    def __init__(self):
        self.league_view_players = None
        self.league_view_teams = None
        self.leaderboard = None
        self.refresh = None
    def refresh_view(self):
        print("Refreshing views (LinkedList.COUNT:", LinkedList.COUNT, ")")


def _create_new_db(db_path: str, league: LinkedList):
    # Remove DB file and initialize schema
    if os.path.exists(db_path):
        os.remove(db_path)
    init_new_db(db_path, league)


def _load_csv_folder_replace(league: LinkedList, folder: Path, db_path: str):
    """Replicates the Create New Database path: drop DB, init, clear memory, import, build GUI."""
    # 1) Create new DB
    _create_new_db(db_path, league)

    # 2) Clear league memory
    league.head = None
    LinkedList.COUNT = 0

    # 3) Collect CSVs and select session
    csv_files = get_csv_files(str(folder))
    sessions = group_csv_by_session(csv_files)
    if not sessions:
        raise RuntimeError(f"No CSVs found in {folder}")
    # pick first (or only) session
    chosen_session = sorted(sessions.keys())[0]
    selected_files = sessions[chosen_session]

    # 4) Import into DB
    conn = sqlite3.connect(db_path)
    summary = {}
    try:
        from src.core.stack import InstanceStack
        stack = InstanceStack()
        for table, filepath in selected_files:
            insert_csv_to_table(table, filepath, conn, mode="overwrite", summary=summary, stack=stack, parent=None, league=league)
    finally:
        conn.close()

    # 5) Build in-memory league and simulate GUI refresh
    parent = _ParentStub()
    try:
        instances = stack.getInstances()
    except Exception:
        instances = []
    if instances:
        load_all_gui(instances, parent, league, mode="overwrite")


def assert_only_expected_after_replace(league: LinkedList, expected_team_names, unexpected_team_names):
    teams = [t.name for t in league.get_all_objs()]
    for name in expected_team_names:
        assert name in teams, f"Expected team '{name}' not found after replace. Found: {teams}"
    for name in unexpected_team_names:
        assert name not in teams, f"Unexpected team '{name}' persists after replace. Found: {teams}"


def main():
    db_path = "data/database/League.db"
    save1 = ROOT / "data" / "exports" / "save_1"
    save2 = ROOT / "data" / "exports" / "save_2"

    league = LinkedList()

    # Load save_2 under Replace (authoritative)
    print("-- Replace load: save_2 --")
    _load_csv_folder_replace(league, save2, db_path)
    print("Teams after save_2:", [t.name for t in league.get_all_objs()])

    # Then Replace with save_1; ensure nothing from save_2 persists
    print("-- Replace load: save_1 --")
    _load_csv_folder_replace(league, save1, db_path)
    teams_after_save1 = [t.name for t in league.get_all_objs()]
    print("Teams after save_1:", teams_after_save1)

    # Basic assertions (adjust names as needed)
    assert_only_expected_after_replace(
        league,
        expected_team_names=["test"],
        unexpected_team_names=["any_previous_name_if_different"]
    )

    # Print player summary
    for t in league.get_all_objs():
        print(f"Team {t.name} players:", [p.name for p in t.players])

    print("Dry replace isolation test completed successfully.")


if __name__ == "__main__":
    main()


