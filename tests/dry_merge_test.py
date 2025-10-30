import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.core.linked_list import LinkedList
from src.core.team import Team
from src.core.player import Player


def _to_int(v):
    try:
        if v is None or v == "":
            return 0
        if isinstance(v, int):
            return v
        if isinstance(v, float):
            return int(v)
        s = str(v).strip().strip('"').strip("'")
        if s == "":
            return 0
        if "." in s:
            return int(float(s))
        return int(s)
    except Exception:
        return 0


def apply_player_row(existing: Player, row: dict):
    # Merge order matching loader: events first, then derived recalcs
    def gi(k):
        return _to_int(row.get(k))

    # 1) hit
    h = gi('hit')
    if h: existing.set_hit(h)

    # 2) components bounded by hits
    s1 = gi('singles')
    if s1: existing.set_singles(s1)
    d2 = gi('doubles')
    if d2: existing.set_doubles(d2)
    t3 = gi('triples')
    if t3: existing.set_triples(t3)
    hr = gi('hr')
    if hr: existing.set_hr(hr)

    # 3) PA non-AB events
    bb = gi('bb')
    if bb: existing.set_bb(bb)
    hbp = gi('hbp')
    if hbp: existing.set_hbp(hbp)
    fc = gi('fielder_choice')
    if fc: existing.set_fielder_choice(fc)

    # 4) Outs affecting AB/PA
    so = gi('so')
    if so: existing.set_so(so)
    sf = gi('sac_fly')
    if sf: existing.set_sac_fly(sf)

    # 5) Cosmetic/counters
    rbi = gi('rbi')
    if rbi: existing.set_rbi(rbi)
    runs = gi('runs')
    if runs: existing.set_runs(runs)

    # Recalculate derived offense
    existing.set_AVG(); existing.set_SLG(); existing.set_BABIP(); existing.set_OBP(); existing.set_ISO()


def load_first_row(csv_path: Path) -> dict:
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            return row
    return {}


def main():
    p1 = ROOT / 'data' / 'exports' / 'save_1' / 'player_10302025.csv'
    p2 = ROOT / 'data' / 'exports' / 'save_2' / 'player_10302025.csv'

    row1 = load_first_row(p1)
    row2 = load_first_row(p2)

    league = LinkedList()
    team = Team(league, 'test', 'mgr', max_roster=999)
    league.add_team(team)
    player = Player('player', _to_int(row1.get('number') or 0), team, league, positions=['catcher','third base'])
    team.add_player(player)

    # Apply rows as deltas (session totals)
    apply_player_row(player, row1)
    apply_player_row(player, row2)

    print('After Merge:')
    print('name:', player.name)
    print('pa:', player.pa)
    print('at_bat:', player.at_bat)
    print('hit:', player.hit)
    print('bb:', player.bb)
    print('hbp:', player.hbp)
    print('so:', player.so)
    print('hr:', player.hr)
    print('rbi:', player.rbi)
    print('runs:', player.runs)
    print('singles:', player.singles)
    print('doubles:', player.doubles)
    print('triples:', player.triples)
    print('sac_fly:', player.sac_fly)
    print('AVG:', player.AVG)
    print('OBP:', player.OBP)
    print('SLG:', player.SLG)
    print('BABIP:', player.BABIP)
    print('ISO:', player.ISO)


if __name__ == '__main__':
    main()


