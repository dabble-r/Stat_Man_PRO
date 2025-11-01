#!/usr/bin/env python3
"""
Verification script for project restructuring
Checks that all expected files and directories exist
"""
import os
from pathlib import Path

def check_path(path, description):
    """Check if a path exists and print result"""
    exists = os.path.exists(path)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    return exists

def main():
    print("="  * 70)
    print("PROJECT STRUCTURE VERIFICATION")
    print("=" * 70)
    
    all_good = True
    
    # Check main directories
    print("\n📁 Main Directories:")
    all_good &= check_path("src/", "Source code directory")
    all_good &= check_path("data/", "Data directory")
    all_good &= check_path("assets/", "Assets directory")
    all_good &= check_path("tests/", "Tests directory")
    all_good &= check_path("docs/", "Documentation directory")
    all_good &= check_path("archive/", "Archive directory")
    
    # Check src subdirectories
    print("\n📦 Source Code Structure:")
    all_good &= check_path("src/core/", "Core business logic")
    all_good &= check_path("src/ui/", "User interface")
    all_good &= check_path("src/ui/dialogs/", "UI dialogs")
    all_good &= check_path("src/ui/views/", "UI views")
    all_good &= check_path("src/ui/styles/", "UI styles")
    all_good &= check_path("src/data/", "Data operations")
    all_good &= check_path("src/data/load/", "Data loading")
    all_good &= check_path("src/data/save/", "Data saving")
    all_good &= check_path("src/visualization/", "Visualization")
    all_good &= check_path("src/utils/", "Utilities")
    all_good &= check_path("src/config/", "Configuration")
    
    # Check key files
    print("\n📄 Key Files:")
    all_good &= check_path("main.py", "Application entry point")
    all_good &= check_path("requirements.txt", "Dependencies file")
    all_good &= check_path(".gitignore", "Git ignore file")
    all_good &= check_path("README.md", "Project README")
    all_good &= check_path("src/__init__.py", "src package init")
    all_good &= check_path("src/ui/main_window.py", "Main window")
    
    # Check core modules
    print("\n🎯 Core Modules:")
    all_good &= check_path("src/core/linked_list.py", "LinkedList class")
    all_good &= check_path("src/core/team.py", "Team class")
    all_good &= check_path("src/core/player.py", "Player class")
    all_good &= check_path("src/core/node.py", "Node class")
    
    # Check data directories
    print("\n💾 Data Directories:")
    all_good &= check_path("data/database/", "Database directory")
    all_good &= check_path("data/exports/", "Exports directory")
    all_good &= check_path("data/images/", "Images directory")
    
    # Check documentation
    print("\n📚 Documentation:")
    all_good &= check_path("docs/RESTRUCTURING_GUIDE.md", "Restructuring guide")
    all_good &= check_path("RESTRUCTURING_SUMMARY.md", "Restructuring summary")
    
    # Summary
    print("\n" + "=" * 70)
    if all_good:
        print("✅ ALL CHECKS PASSED! Structure is complete.")
    else:
        print("❌ SOME CHECKS FAILED! Review the output above.")
    print("=" * 70)
    
    # Additional info
    print("\n📊 Statistics:")
    src_files = sum(1 for _ in Path("src").rglob("*.py"))
    print(f"  Python files in src/: {src_files}")
    
    init_files = list(Path("src").rglob("__init__.py"))
    print(f"  __init__.py files: {len(init_files)}")
    
    print("\n🚀 Next Steps:")
    print("  1. Test the application: python main.py")
    print("  2. Verify all features work correctly")
    print("  3. Review RESTRUCTURING_SUMMARY.md")
    print("  4. After successful testing, remove old directories")
    
    return all_good

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

