from src.ui.main_window import MainWindow
from PySide6.QtWidgets import QApplication
from src.utils.img_repo import CreateDir
from src.ui.styles.stylesheets import StyleSheets
import sys 
import os
from pathlib import Path
import sqlite3

def clear_database_on_startup():
    """Clear all data from database on startup - database doesn't persist between sessions"""
    db_path = Path("data/database/League.db")
    
    if not db_path.exists():
        print("No database to clear on startup.")
        return
    
    try:
        print(f"Clearing database on startup: {db_path}")
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = cursor.fetchall()
        
        # Drop all tables
        for table in tables:
            table_name = table[0]
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            print(f"  Dropped table: {table_name}")
        
        conn.commit()
        conn.close()
        print("Database cleared successfully.")
        
    except Exception as e:
        print(f"Error clearing database on startup: {e}")

if __name__ == "__main__":
    # Clear database before starting application
    clear_database_on_startup()
    
    app = QApplication(sys.argv)
    styles = StyleSheets()
    app.setStyleSheet(styles.get_monochrome_1_style())

    window = MainWindow(app)

    sys.exit(app.exec())




