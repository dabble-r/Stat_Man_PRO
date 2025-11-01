# Project Restructuring Guide

## Overview

This document outlines the project restructuring completed on October 30, 2025.

## Changes Made

### 1. New Directory Structure

Created a professional, scalable directory structure:
- `src/` - All source code
- `data/` - Runtime data (renamed from `Saved/`)
- `assets/` - Static assets
- `tests/` - Unit tests
- `docs/` - Documentation
- `archive/` - Deprecated code

### 2. Modular Organization

#### Core Business Logic (`src/core/`)
- Moved from `League/`
- Contains: `linked_list.py`, `team.py`, `player.py`, `node.py`, `game.py`, `stack.py`

#### User Interface (`src/ui/`)
- **Dialogs** (`src/ui/dialogs/`) - Consolidated from 8 separate folders
- **Views** (`src/ui/views/`) - Main view components from `start_page/` and `TabWidget/`
- **Styles** (`src/ui/styles/`) - Application themes

#### Data Operations (`src/data/`)
- **Load** (`src/data/load/`) - CSV import functionality
- **Save** (`src/data/save/`) - Database and CSV export

#### Visualization (`src/visualization/`)
- Moved from `Graph/`
- Contains chart and graph components

#### Utilities (`src/utils/`)
- Consolidated from `Files/`, `Mouse_Events/`, `Undo/`, `refresh/`
- Common utilities and helpers

### 3. Path Updates

| Old Path | New Path |
|----------|----------|
| `Saved/DB/` | `data/database/` |
| `Saved/CSV/` | `data/exports/` |
| `Saved/Images/` | `data/images/` |
| `Icon/` | `assets/icons/` |

### 4. Import Updates

All imports have been updated to use the new structure:

**Before:**
```python
from League.team import Team
from start_page.league_view_teams import LeagueViewTeams
from Save.save import Save
```

**After:**
```python
from src.core.team import Team
from src.ui.views.league_view_teams import LeagueViewTeams
from src.data.save.save import Save
```

## Migration Details

### Files Moved

1. **Core**: All files from `League/` → `src/core/`
2. **UI Dialogs**: 
   - `add_player/` → `src/ui/dialogs/`
   - `add_team/` → `src/ui/dialogs/`
   - `stat_dialog/` → `src/ui/dialogs/`
   - `update_dialog/` → `src/ui/dialogs/`
   - `CloseDialog/` → `src/ui/dialogs/`
   - `remove/` → `src/ui/dialogs/`
   - `Message/` → `src/ui/dialogs/`
   - `Add_Save/` → `src/ui/dialogs/`

3. **UI Views**:
   - `start_page/` → `src/ui/views/`
   - `TabWidget/` → `src/ui/views/`

4. **Data**:
   - `Load/` → `src/data/load/`
   - `Save/` → `src/data/save/`

5. **Visualization**:
   - `Graph/` → `src/visualization/`

6. **Utilities**:
   - `Files/` → `src/utils/`
   - `Mouse_Events/` → `src/utils/`
   - `Undo/` → `src/utils/`
   - `refresh/` → `src/utils/`
   - `view_db.py` → `src/utils/`

### Automated Updates

Created `update_imports.py` script that automatically:
- Updated 26 files with new import paths
- Replaced old path strings with new paths
- Maintained code functionality

## Benefits

### 1. Better Organization
- Clear separation of concerns
- Logical grouping of related functionality
- Easier navigation

### 2. Scalability
- Room for growth in each module
- Easy to add new features
- Standard Python package structure

### 3. Maintainability
- Reduced coupling between modules
- Clear dependencies
- Professional structure

### 4. Development
- Easier onboarding for new developers
- Standard conventions
- Ready for testing framework

## Backward Compatibility

### Old Structure Still Present

The original directories still exist to ensure no data loss:
- Original `League/`, `Load/`, `Save/` folders remain
- Original `Saved/` folder with existing data remains
- Can be safely removed after verifying new structure works

### Testing Required

Before removing old directories:
1. Test all major features:
   - Create/add teams and players
   - Load from CSV
   - Save to database and CSV
   - Remove items
   - Refresh views
   - Statistics dialogs

2. Verify data paths:
   - Check `data/database/League.db` is created/used
   - Check CSV exports go to `data/exports/`
   - Check images load from `data/images/`

## Next Steps

### Immediate (Completed)
- ✅ Create new directory structure
- ✅ Move all files
- ✅ Update imports
- ✅ Create __init__.py files
- ✅ Create .gitignore
- ✅ Create requirements.txt
- ✅ Update README.md

### Short Term (Recommended)
- Test all functionality thoroughly
- Remove old directories after verification
- Add unit tests in `tests/`
- Create API documentation

### Long Term
- Implement configuration system in `src/config/`
- Add comprehensive test coverage
- Create developer documentation
- Set up CI/CD pipeline

## Troubleshooting

### Import Errors

If you see import errors:
```bash
python update_imports.py
```

### Path Errors

If the application can't find data files:
1. Check that `data/` directory exists
2. Verify paths in main.py point to `data/database/League.db`
3. Check database path in `src/ui/main_window.py`

### Old vs New Paths

Current locations:
- Database: `data/database/League.db` (was `Saved/DB/League.db`)
- Exports: `data/exports/` (was `Saved/CSV/`)
- Images: `data/images/` (was `Saved/Images/`)

## Rollback Plan

If issues arise:

1. **Revert main.py imports:**
   ```python
   from MainWindow.main_window import MainWindow
   from Styles.stylesheets import StyleSheets
   # etc.
   ```

2. **Use git to restore:**
   ```bash
   git checkout HEAD~1 main.py
   ```

3. **Old structure is still intact** - just update paths back

## Files Created

- `src/` directory structure with all modules
- `data/` directory structure
- `assets/` directory structure
- `.gitignore`
- `requirements.txt`
- `README.md` (updated)
- `update_imports.py` (utility script)
- `docs/RESTRUCTURING_GUIDE.md` (this file)

## Verification Checklist

- [ ] Application launches without errors
- [ ] Can create new team
- [ ] Can add player to team
- [ ] Can save to database
- [ ] Can export to CSV
- [ ] Can load from CSV
- [ ] Can remove items
- [ ] Statistics dialogs work
- [ ] Images load correctly
- [ ] Graphs display properly

---

**Date Completed:** October 30, 2025  
**Implemented By:** AI Assistant  
**Verified By:** [Pending]

