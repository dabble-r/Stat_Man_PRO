# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for stat_man_g Windows executable build.
This creates a standalone .exe that includes Python interpreter and all dependencies.
"""

import sys
from pathlib import Path

block_cipher = None

# Base directory for resolving paths
base_dir = Path('.')

# Icon handling - Pillow is required for icon conversion/validation
# If icon file exists, use it (Pillow will handle conversion if needed)
icon_path = Path('assets/icons/favicon.ico')
if icon_path.exists():
    app_icon = str(icon_path)
else:
    app_icon = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),  # Bundle assets directory
    ],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtWidgets',
        'PySide6.QtGui',
        'sqlite3',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'IPython',
        'jupyter',
        'pytest',
        'setuptools',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Build EXE with icon support (Pillow handles icon conversion)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='stat_man_g',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=app_icon if app_icon is not None else None,
)

