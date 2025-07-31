# Building Standalone Executables for Gallery-DL GUI

This guide explains how to create standalone executable files for the Gallery-DL GUI that users can download and run without any Python installation.

## Overview

We'll use PyInstaller to create standalone executables that include:
- Python interpreter
- All required dependencies (gallery-dl, requests, Pillow)
- The complete GUI application
- All necessary files and resources

## Prerequisites

- Python 3.8+ installed on the build machine
- All project dependencies installed
- PyInstaller package

## Quick Setup

### 1. Install PyInstaller
```bash
pip install pyinstaller
```

### 2. Build the Executable
```bash
# For Windows
python build_executable.py --platform windows

# For Linux
python build_executable.py --platform linux

# For macOS
python build_executable.py --platform macos
```

### 3. Find Your Executable
- **Windows**: `dist/Gallery-DL-GUI.exe`
- **Linux**: `dist/Gallery-DL-GUI`
- **macOS**: `dist/Gallery-DL-GUI.app`

## Build Script Usage

The `build_executable.py` script provides several options:

```bash
# Basic build
python build_executable.py

# Build with console (for debugging)
python build_executable.py --console

# Build with custom name
python build_executable.py --name "MyGalleryDL"

# Clean build (removes old builds first)
python build_executable.py --clean

# Build for specific platform
python build_executable.py --platform windows
```

## Manual PyInstaller Commands

If you prefer to run PyInstaller directly:

### Windows
```bash
pyinstaller --onefile --windowed --name "Gallery-DL-GUI" ^
    --add-data "supportedsites.md;." ^
    --add-data "models;models" ^
    --add-data "views;views" ^
    --add-data "controllers;controllers" ^
    --add-data "utils;utils" ^
    --hidden-import "gallery_dl" ^
    --hidden-import "requests" ^
    --hidden-import "PIL" ^
    --icon "icon.ico" ^
    gallery_dl_gui.py
```

### Linux/macOS
```bash
pyinstaller --onefile --windowed --name "Gallery-DL-GUI" \
    --add-data "supportedsites.md:." \
    --add-data "models:models" \
    --add-data "views:views" \
    --add-data "controllers:controllers" \
    --add-data "utils:utils" \
    --hidden-import "gallery_dl" \
    --hidden-import "requests" \
    --hidden-import "PIL" \
    gallery_dl_gui.py
```

## GitHub Release Workflow

### 1. Tag a Release
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### 2. Build Executables
```bash
# Build for all platforms (if you have access to each)
python build_executable.py --platform windows
python build_executable.py --platform linux
python build_executable.py --platform macos
```

### 3. Create GitHub Release
1. Go to your GitHub repository
2. Click "Releases" → "Create a new release"
3. Select your tag (v1.0.0)
4. Upload the executable files:
   - `Gallery-DL-GUI-Windows.exe`
   - `Gallery-DL-GUI-Linux`
   - `Gallery-DL-GUI-macOS.app.zip`

## File Sizes and Performance

**Expected file sizes:**
- Windows: ~50-80 MB
- Linux: ~45-70 MB
- macOS: ~55-85 MB

**Startup time:**
- First run: 3-8 seconds (extracting embedded files)
- Subsequent runs: 1-3 seconds

## Troubleshooting

### Common Issues

**"Failed to execute script" error:**
- Run with `--console` flag to see error messages
- Check for missing dependencies

**Large file size:**
- This is normal for standalone executables
- PyInstaller includes the entire Python runtime

**Antivirus false positives:**
- Common with PyInstaller executables
- Submit to antivirus vendors as false positive

### Debugging

1. **Build with console:**
   ```bash
   python build_executable.py --console
   ```

2. **Check dependencies:**
   ```bash
   pyi-archive_viewer dist/Gallery-DL-GUI.exe
   ```

3. **Test in clean environment:**
   - Test on a machine without Python installed
   - Verify all features work correctly

## Advanced Configuration

### Custom Icon
Place an `icon.ico` file in the project root, and the build script will automatically include it.

### Excluding Modules
Edit `build_executable.py` to exclude unnecessary modules:
```python
excludes = ['matplotlib', 'scipy', 'numpy']  # Add modules to exclude
```

### Including Additional Files
Add more files in the build script:
```python
datas = [
    ('config/*', 'config'),
    ('templates/*', 'templates'),
]
```

## Distribution

### Recommended Release Format

**GitHub Release Structure:**
```
Gallery-DL-GUI-v1.0.0/
├── Gallery-DL-GUI-Windows-x64.exe
├── Gallery-DL-GUI-Linux-x64
├── Gallery-DL-GUI-macOS-x64.app.zip
├── README.md
└── CHANGELOG.md
```

### User Instructions
Include these instructions with your release:

1. **Download** the appropriate file for your operating system
2. **Windows**: Double-click the `.exe` file
3. **Linux**: Make executable and run: `chmod +x Gallery-DL-GUI-Linux && ./Gallery-DL-GUI-Linux`
4. **macOS**: Extract and run the `.app` file

## Automation with GitHub Actions

The project includes GitHub Actions workflow for automatic builds on new releases. See `.github/workflows/build-release.yml` for details.
