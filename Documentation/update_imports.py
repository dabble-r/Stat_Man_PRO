#!/usr/bin/env python3
"""
Script to update all import statements after project restructuring
"""
import os
import re

# Define import mappings: old_import -> new_import
IMPORT_MAPPINGS = {
    # Core modules
    'from League.linked_list import': 'from src.core.linked_list import',
    'from League.team import': 'from src.core.team import',
    'from League.player import': 'from src.core.player import',
    'from League.node import': 'from src.core.node import',
    'from League.game import': 'from src.core.game import',
    'from League.stack import': 'from src.core.stack import',
    
    # UI Views
    'from start_page.league_view_players import': 'from src.ui.views.league_view_players import',
    'from start_page.league_view_teams import': 'from src.ui.views.league_view_teams import',
    'from start_page.leaderboard_ui import': 'from src.ui.views.leaderboard_ui import',
    'from start_page.selection import': 'from src.ui.views.selection import',
    'from TabWidget': 'from src.ui.views',
    
    # UI Dialogs
    'from add_player': 'from src.ui.dialogs',
    'from add_team': 'from src.ui.dialogs',
    'from stat_dialog': 'from src.ui.dialogs',
    'from update_dialog': 'from src.ui.dialogs',
    'from CloseDialog.close import': 'from src.ui.dialogs.close import',
    'from remove.remove import': 'from src.ui.dialogs.remove import',
    'from Message.message import': 'from src.ui.dialogs.message import',
    'from Add_Save.add_save_ui import': 'from src.ui.dialogs.add_save_ui import',
    
    # UI Styles
    'from Styles.stylesheets import': 'from src.ui.styles.stylesheets import',
    
    # Data operations
    'from Load.load_csv import': 'from src.data.load.load_csv import',
    'from Load.load import': 'from src.data.load.load import',
    'from Save.save import': 'from src.data.save.save import',
    'from Save.save_csv import': 'from src.data.save.save_csv import',
    'from Save.save_dialog_ui import': 'from src.data.save.save_dialog_ui import',
    'from Save.save_exp import': 'from src.data.save.save_exp import',
    
    # Visualization
    'from Graph.bar_graph import': 'from src.visualization.bar_graph import',
    'from Graph.donut_graph import': 'from src.visualization.donut_graph import',
    'from Graph.graph_window import': 'from src.visualization.graph_window import',
    
    # Utils
    'from Files.file_dialog import': 'from src.utils.file_dialog import',
    'from Files.image_window import': 'from src.utils.image_window import',
    'from Files.image import': 'from src.utils.image import',
    'from Files.img_repo import': 'from src.utils.img_repo import',
    'from Mouse_Events.tree_event_filter import': 'from src.utils.tree_event_filter import',
    'from Undo.undo import': 'from src.utils.undo import',
    'from refresh.refresh import': 'from src.utils.refresh import',
}

# Path mappings for string literals
PATH_MAPPINGS = {
    '"Saved/DB': '"data/database',
    '"Saved/CSV': '"data/exports',
    '"Saved/Images': '"data/images',
    "'Saved/DB": "'data/database",
    "'Saved/CSV": "'data/exports",
    "'Saved/Images": "'data/images",
}

def update_file(filepath):
    """Update imports and paths in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Update imports
        for old_import, new_import in IMPORT_MAPPINGS.items():
            content = content.replace(old_import, new_import)
        
        # Update path strings
        for old_path, new_path in PATH_MAPPINGS.items():
            content = content.replace(old_path, new_path)
        
        # Only write if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {filepath}")
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def process_directory(directory):
    """Process all Python files in a directory"""
    updated_count = 0
    for root, dirs, files in os.walk(directory):
        # Skip __pycache__ and archived directories
        dirs[:] = [d for d in dirs if d not in ['__pycache__', 'myenv', 'archive', '.git']]
        
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                if update_file(filepath):
                    updated_count += 1
    return updated_count

if __name__ == '__main__':
    print("Starting import updates...")
    print("=" * 60)
    
    # Update files in src/
    src_count = process_directory('src')
    print(f"\nUpdated {src_count} files in src/")
    
    print("\n" + "=" * 60)
    print("Import update complete!")

