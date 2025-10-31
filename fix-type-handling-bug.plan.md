# Fix Type Handling Bug for Player and Team Stats

## Bug Summary

When loading player data from CSV files, numeric statistics (hit, so, runs, p_so) are stored as strings instead of integers. When team aggregation methods (`get_team_hits()`, `get_team_so()`, `get_team_runs()`, `get_team_k()`) attempt to sum these values, Python raises `TypeError: unsupported operand type(s) for +=: 'int' and 'str'`.

## Root Cause

In `src/data/load/load_csv.py`, when loading players from CSV:

1. **Line 733**: `load_player_gui(attr, val, player)` is called with CSV values that are strings
2. **Line 1119-1121**: `load_player_gui()` simply does `setattr(player, attr, val)`, which sets attributes like `player.hit` to string values (e.g., `"5"` instead of `5`)
3. **Team aggregation methods** (`src/core/team.py` lines 286, 294, 302, 323): These methods directly add player stats without type conversion:
   - `get_team_hits()`: `total += player.hit` 
   - `get_team_so()`: `total += player.so`
   - `get_team_runs()`: `total += player.runs`
   - `get_team_k()`: `total += player.p_so`
4. Note: `get_team_era()` (line 312) correctly converts: `era_float = float(player.era)` - this is safe

The codebase already has:
- `_to_int()` helper function (lines 36-53) that safely converts strings to int
- `_normalize_numeric_attrs()` function (lines 55-62) that normalizes numeric attributes
- These are used in merge mode but NOT when initially loading CSV data

## Solution

Fix in two places for robustness:

### 1. Fix Root Cause: Convert Types During CSV Load

**File**: `src/data/load/load_csv.py`

**Location**: Lines 730-733 (in `load_all_gui()` function, player loading section)

When setting numeric player attributes from CSV, convert string values to integers using the existing `_to_int()` helper:

```python
else:
    if val in (0, '0', 0.0, '0.0'):
        continue
    # Convert numeric stats to proper types when loading from CSV
    if attr in PLAYER_NUMERIC_ADD:
        load_player_gui(attr, _to_int(val), player)
    elif attr in PLAYER_DERIVED:
        try:
            load_player_gui(attr, float(val) if val not in (0, '0', 0.0, '0.0', '') else 0.0, player)
        except Exception:
            load_player_gui(attr, 0.0, player)
    else:
        load_player_gui(attr, val, player)
```

Apply the same fix for pitchers at lines 882-885 (pitcher loading section).

### 2. Make Team Aggregation Methods Defensive

**File**: `src/core/team.py`

Make the team stat aggregation methods defensive by converting values before arithmetic operations:

- **Line 286** (`get_team_hits()`): Convert `player.hit` to int before adding
- **Line 294** (`get_team_so()`): Convert `player.so` to int before adding  
- **Line 302** (`get_team_runs()`): Convert `player.runs` to int before adding
- **Line 323** (`get_team_k()`): Convert `player.p_so` to int before adding

Create a helper function to safely convert player stat to int:

```python
def _to_int_safe(val):
    """Safely convert value to int, returning 0 on failure."""
    try:
        if val is None:
            return 0
        if isinstance(val, int):
            return val
        if isinstance(val, float):
            return int(val)
        return int(float(str(val).strip()))
    except Exception:
        return 0
```

Then update each aggregation method:
- `total += _to_int_safe(player.hit)`
- `total += _to_int_safe(player.so)`
- `total += _to_int_safe(player.runs)`
- `total += _to_int_safe(player.p_so)`

## Testing

After fix, verify that:
1. Loading CSV with player stats displays and calculates correctly
2. Team aggregation methods work with both int and string values (defensive coding)
3. Graph generation in stat dialog works without TypeError
4. No regression in database loading (which already converts properly)

