@echo off
REM Quick build script for Gallery-DL GUI executables (Windows)
REM This script provides an easy way to build executables on Windows

echo Gallery-DL GUI - Quick Build Script (Windows)
echo ==============================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.8+ first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Using Python: 
python --version

REM Install build requirements
echo Installing build requirements...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller

if errorlevel 1 (
    echo Error: Failed to install requirements
    pause
    exit /b 1
)

REM Build executable
echo Building executable for Windows...
python build_executable.py --platform windows --clean

if errorlevel 1 (
    echo Error: Build failed
    pause
    exit /b 1
)

echo.
echo Build completed!
echo Check the 'dist' directory for your executable.

REM Show file info if build was successful
if exist "dist" (
    echo.
    echo Built files:
    dir dist /b
)

echo.
echo Press any key to exit...
pause >nul
