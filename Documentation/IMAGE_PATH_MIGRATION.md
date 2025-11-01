# Image Path Migration - Complete! ✅

**Date:** October 30, 2025  
**Issue:** Team/player images not displaying in GUI after restructuring

## Problem

After restructuring the project:
- Old CSV/database files contained paths like: `/home/njbro/stat_man_g/Saved/Images/quartet-west.jpg`
- But images were moved to: `/home/njbro/stat_man_g/data/images/quartet-west.jpg`
- When loading from CSV, old paths were loaded as-is
- `create_icon()` tried to load from non-existent path
- Result: Images didn't display (but no error due to previous None-check fix)

## Solution

Added automatic path migration during CSV/database loading.

### New Function Added

**File:** `src/data/load/load_csv.py` (lines 30-62)

```python
def migrate_image_path(old_path):
    """
    Migrate old image paths (Saved/Images/) to new paths (data/images/).
    
    Handles:
    - Old paths: Saved/Images/file.jpg → data/images/file.jpg
    - Relative paths: file.jpg → data/images/file.jpg
    - Already migrated paths: data/images/file.jpg → data/images/file.jpg
    """
```

**Logic:**
1. Check if path contains old `Saved/Images` structure
2. Extract filename from old path
3. Build new path: `{cwd}/data/images/{filename}`
4. Return migrated path

### Applied to 3 Locations

#### 1. Team Logo Loading (Line 392)
```python
elif attr == 'logo':
    # Migrate old Saved/Images paths to new data/images paths
    migrated_path = migrate_image_path(val)
    if migrated_path:
        load_team_gui(attr, migrated_path, team)
    else:
        team.logo = None
```

#### 2. Player Image Loading (Line 540)
```python
elif attr == 'image':
    # Migrate old Saved/Images paths to new data/images paths
    migrated_path = migrate_image_path(val)
    if migrated_path:
        player.image = migrated_path
    else:
        player.image = None
```

#### 3. Pitcher Image Loading (Line 632)
```python
elif attr == 'image':
    # Migrate old Saved/Images paths to new data/images paths
    migrated_path = migrate_image_path(val)
    if migrated_path:
        pitcher.image = migrated_path
    else:
        pitcher.image = None
```

## How It Works

### Before Migration
```
CSV contains: /home/njbro/stat_man_g/Saved/Images/quartet-west.jpg
File exists at: /home/njbro/stat_man_g/data/images/quartet-west.jpg
Result: ❌ Image not found, doesn't display
```

### After Migration
```
CSV contains: /home/njbro/stat_man_g/Saved/Images/quartet-west.jpg
migrate_image_path() converts to: /home/njbro/stat_man_g/data/images/quartet-west.jpg
File exists at: /home/njbro/stat_man_g/data/images/quartet-west.jpg
Result: ✅ Image loads and displays correctly!
```

## Console Output

When loading old CSV files, you'll now see:
```
Migrating image path: /home/njbro/stat_man_g/Saved/Images/quartet-west.jpg -> /home/njbro/stat_man_g/data/images/quartet-west.jpg
```

This confirms the path is being migrated automatically.

## Supported Path Formats

The migration function handles:

1. **Old absolute paths:**
   ```
   /home/njbro/stat_man_g/Saved/Images/file.jpg
   → /home/njbro/stat_man_g/data/images/file.jpg
   ```

2. **Old relative paths:**
   ```
   Saved/Images/file.jpg
   → /home/njbro/stat_man_g/data/images/file.jpg
   ```

3. **Windows-style paths:**
   ```
   C:\stat_man_g\Saved\Images\file.jpg
   → /home/njbro/stat_man_g/data/images/file.jpg
   ```

4. **Just filenames:**
   ```
   file.jpg
   → /home/njbro/stat_man_g/data/images/file.jpg
   ```

5. **Already migrated:**
   ```
   /home/njbro/stat_man_g/data/images/file.jpg
   → /home/njbro/stat_man_g/data/images/file.jpg (no change)
   ```

## Backward Compatibility

✅ **Old CSV files:** Automatically migrated on load  
✅ **New CSV files:** Work as expected  
✅ **Mixed data:** Both old and new paths handled  
✅ **No manual intervention:** Migration happens transparently

## Testing

After this fix, images should display correctly when:

1. **Loading from old CSV files**
   - CSV has old `Saved/Images/` paths
   - Images migrated to `data/images/`
   - ✅ Should display correctly now

2. **Loading from new CSV files**
   - CSV has new `data/images/` paths
   - ✅ Should display correctly (no migration needed)

3. **Creating new teams/players**
   - New images saved with `data/images/` paths
   - ✅ Should display correctly

## What to Do Now

1. **Load your old CSV data**
   ```bash
   python main.py
   # Click Load → Select old CSV folder
   ```

2. **Check console for migration messages**
   ```
   Migrating image path: Saved/Images/... -> data/images/...
   ```

3. **View team/player stats**
   - Images should now display correctly! 🎉

4. **Re-save to update database** (optional)
   - This will update paths in database to new format
   - Future loads will be faster (no migration needed)

## Files Changed

- ✅ `src/data/load/load_csv.py` - Added migration function and applied to all image/logo loading

## Summary

**Problem:** Old paths → Images don't exist → No display  
**Solution:** Automatic path migration → Correct paths → Images display! ✅

The application now seamlessly handles old and new path formats, ensuring all images display correctly regardless of when the data was saved.

---

**🎉 Images should now display correctly in the statistics dialog!**

