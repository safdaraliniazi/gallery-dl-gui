@echo off
REM Gallery-DL GUI Setup Script for Windows
REM This script helps set up the optimal environment for browser preview functionality

echo.
echo ========================================
echo Gallery-DL GUI Environment Setup
echo ========================================
echo.

REM Check current Python version
echo Checking current Python version...
python --version 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Python not found in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo.
echo Checking for Python 3.9 (recommended for browser preview)...
py -3.9 --version 2>nul
if %errorlevel% neq 0 (
    echo Python 3.9 not found.
    echo.
    echo For full browser preview functionality, install Python 3.9:
    echo   winget install Python.Python.3.9
    echo.
    echo Continuing with current Python version...
    echo Note: Browser preview may show fallback display if not Python 3.8-3.9
    set USE_CURRENT_PYTHON=1
) else (
    echo Python 3.9 found! This is optimal for browser preview.
    set USE_CURRENT_PYTHON=0
)

echo.
echo Setting up virtual environment...

if %USE_CURRENT_PYTHON%==1 (
    python -m venv gdlgui_env
) else (
    py -3.9 -m venv gdlgui_env
)

if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo Activating virtual environment...
call gdlgui_env\Scripts\activate.bat

echo Installing dependencies...
pip install gallery-dl cefpython3

if %errorlevel% neq 0 (
    echo WARNING: Some packages may have failed to install
    echo This is normal if CEF Python doesn't support your Python version
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To run the application:
echo   1. Activate the environment: gdlgui_env\Scripts\activate
echo   2. Run the application: python gallery_dl_gui.py
echo.
echo For browser preview functionality:
echo   - Works best with Python 3.8-3.9
echo   - Shows informative fallback for other versions
echo   - All core functionality works regardless of Python version
echo.
pause
