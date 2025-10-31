@echo off
REM Build script for creating Windows executable
REM This script builds the stat_man_g.exe using PyInstaller

echo Building stat_man_g.exe...
echo.

REM Install/upgrade required build dependencies from requirements.txt
echo Installing required dependencies...
pip install -q pyinstaller>=6.0.0 pillow>=10.0.0
if errorlevel 1 (
    echo Failed to install required dependencies. Please install manually:
    echo   pip install pyinstaller pillow
    pause
    exit /b 1
)

REM Verify Pillow is installed (required for icon processing)
python -c "import PIL" 2>nul
if errorlevel 1 (
    echo ERROR: Pillow installation failed. Please install manually:
    echo   pip install pillow
    pause
    exit /b 1
)

REM Clean previous build to avoid cached icon issues
echo Cleaning previous build...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Run PyInstaller
echo Running PyInstaller...
pyinstaller --clean stat_man_g.spec

if errorlevel 1 (
    echo.
    echo Build failed! Check the output above for errors.
    pause
    exit /b 1
)

echo.
echo Build successful!
echo Executable created at: dist\stat_man_g.exe
echo.
pause

