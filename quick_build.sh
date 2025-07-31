#!/bin/bash

# Quick build script for Gallery-DL GUI executables
# This script provides an easy way to build executables for different platforms

set -e  # Exit on any error

echo "Gallery-DL GUI - Quick Build Script"
echo "=================================="

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "Error: Python not found. Please install Python 3.8+ first."
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

echo "Using Python: $PYTHON_CMD"

# Install build requirements if not already installed
echo "Installing build requirements..."
$PYTHON_CMD -m pip install --upgrade pip
$PYTHON_CMD -m pip install -r requirements.txt
$PYTHON_CMD -m pip install pyinstaller

# Add local bin to PATH for PyInstaller
export PATH="$HOME/.local/bin:$PATH"

# Detect platform
PLATFORM=""
case "$(uname -s)" in
    Linux*)     PLATFORM="linux";;
    Darwin*)    PLATFORM="macos";;
    CYGWIN*|MINGW*|MSYS*) PLATFORM="windows";;
    *)          PLATFORM="auto";;
esac

echo "Detected platform: $PLATFORM"

# Build executable
echo "Building executable..."
$PYTHON_CMD build_executable.py --platform $PLATFORM --clean

echo ""
echo "Build completed!"
echo "Check the 'dist/' directory for your executable."

# Show file info if build was successful
if [ -d "dist" ]; then
    echo ""
    echo "Built files:"
    ls -lh dist/
fi
