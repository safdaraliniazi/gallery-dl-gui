# Gallery-DL GUI

A modern graphical user interface for [gallery-dl](https://github.com/mikf/gallery-dl), the command-line program to download image galleries and collections from various image hosting sites.

## Features

- **User-friendly interface** - Clean, modern GUI built with tkinter
- **Multi-site support** - Works with 300+ websites supported by gallery-dl
- **Download options** - Configure download paths, extract URLs only, write metadata
- **Authentication support** - Username/password and cookies file support
- **URL testing** - Test URLs before downloading
- **Real-time progress** - Live output log and progress tracking
- **Settings persistence** - Save and load your preferences
- **Comprehensive site support** - Full searchable list of 300+ supported websites
- **Web preview functionality** - Click any supported site to preview it (requires Python 3.12 or earlier for browser preview, fallback available)
- **Enhanced window layout** - Larger, resizable interface with maximized startup
- **Error descriptions** - Clear explanations for download failures with exit codes
- **Easy installation** - Simple Python application with minimal dependencies

## Compatibility

- **Python Version**: 3.8+ (Recommended: 3.9 for full browser preview support)
- **Operating Systems**: Windows, macOS, Linux
- **Browser Preview**: Available with Python 3.8-3.9 + CEF Python v66.1
- **Note**: CEF Python v66.1 supports Python 3.8-3.9 on Windows. For Python 3.10+ users, browser preview shows an informative fallback display

## Supported Sites

Gallery-dl supports downloads from:
- Social media: Twitter, Instagram, Tumblr
- Art platforms: DeviantArt, Pixiv, ArtStation
- Image boards: Danbooru, Gelbooru, e621
- Manga sites: MangaDex, Dynasty Reader
- And 300+ more sites

## Installation

### Prerequisites

1. **Python 3.8+** - Download from [python.org](https://www.python.org/downloads/)
2. **Gallery-dl** - The underlying download engine

### Setup

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install gallery-dl:
   ```bash
   pip install gallery-dl
   ```

## Project Structure

The application follows the Model-View-Controller (MVC) design pattern:

```
gdlgui/
├── gallery_dl_gui.py          # Main entry point
├── controllers/               # Business logic and coordination
├── models/                    # Data models and state management
├── views/                     # User interface components
├── utils/                     # Utility functions and services
└── ARCHITECTURE.md           # Detailed architecture documentation
```

For detailed architecture information, see [ARCHITECTURE.md](ARCHITECTURE.md).

## Usage

### Running the Application

You have multiple options to run the application:

#### Option 1: Launcher (Recommended)
```bash
# Double-click launcher.bat on Windows
launcher.bat
```

#### Option 2: Direct execution
```bash
python gallery_dl_gui.py
```

#### Option 3: Using VS Code
- Open the project in VS Code
- Use Ctrl+Shift+P and search for "Tasks: Run Task"
- Select "Run Gallery-DL GUI"

### Using the GUI

1. **Enter URL** - Paste the URL of the gallery/image you want to download
2. **Choose download path** - Select where to save the files
3. **Configure options**:
   - Extract URLs only: Get direct image links without downloading
   - No download (test): Test the URL without actually downloading
   - Write info JSON: Save metadata about downloaded files
4. **Authentication tab** - Username/password and cookies file support for sites requiring login
5. **URL testing** - Test URLs before downloading to verify they work
6. **Click Download** - Start the download process
7. **Monitor progress** - Watch the real-time log output
8. **Explore websites** - Use the About tab to discover and preview supported sites

### New Web Preview Features

- **Site Discovery** - Browse 300+ supported websites in the About tab
- **Web Preview** - Click any site to see a preview with website information
- **Quick Access** - Double-click sites to open them in your browser
- **Enhanced Layout** - Larger window with resizable panels for better viewing

### Features

- **URL history** - Dropdown with previously used URLs
- **Settings persistence** - Your preferences are automatically saved
- **Quick actions** - Direct links to documentation and folder access
- **Comprehensive site list** - Searchable database of 300+ supported websites with categories
- **Detailed error reporting** - Clear explanations for download failures

### Example URLs

- Twitter post: `https://twitter.com/username/status/123456789`
- DeviantArt gallery: `https://www.deviantart.com/artist/gallery`
- Pixiv artwork: `https://www.pixiv.net/en/artworks/123456`
- Instagram post: `https://www.instagram.com/p/ABC123/`

## Configuration

The application will automatically detect gallery-dl installation and display version information in the log.

For advanced gallery-dl configuration, you can create a `gallery-dl.conf` file in your user directory following the [official documentation](https://gdl-org.github.io/docs/configuration.html).

## Troubleshooting

### Gallery-dl not found
If you see "Gallery-dl not found" in the log:
```bash
pip install gallery-dl
```

### Common Error Codes
When downloads fail, the GUI now provides clear explanations:
- **Exit code 4**: Input/output error (network issues, file permissions, or unsupported URL)
- **Exit code 6**: Authentication error (invalid credentials or login required)
- **Exit code 8**: Format or extraction error (unsupported site or changed website structure)
- **Exit code 16**: File system error (disk full, permission denied, or path issues)
- **Exit code 64**: Unsupported URL or site (the website is not supported by gallery-dl)

### Unsupported Websites
Some websites are not supported by gallery-dl, including:
- **Commercial stock photo sites**: Shutterstock, Getty Images, Adobe Stock
- **Paid subscription services**: Many premium content sites
- **Sites with complex anti-bot protection**: Some newer social media features

For a complete list of supported sites, check the "About" tab in the Advanced GUI.

### Test URL shows "file not found" error
The GUI automatically handles this by trying different ways to run gallery-dl:
1. First tries the `gallery-dl` command directly
2. Falls back to `python -m gallery_dl` if the direct command fails
3. Both the Test URL and Download functions use the same fallback mechanism

### Download fails
- Check if the URL is supported by gallery-dl
- Verify internet connection
- Some sites may require authentication (cookies/login)
- Try testing the URL first using the "Test URL" button (Advanced GUI)

### Permission errors
- Make sure you have write permission to the download directory
- Try running as administrator on Windows if needed

## Features in Detail

### Download Options
- **Extract URLs only (-g)**: Get direct links without downloading files
- **No download (--no-download)**: Test URLs and see what would be downloaded
- **Write info JSON (--write-info-json)**: Save metadata alongside downloads

### Real-time Monitoring
- Live output from gallery-dl command
- Progress indication during downloads
- Timestamp for all log entries
- Stop downloads at any time

### Path Management
- Browse and select download directories
- Automatic directory creation
- Remember last used paths

## License

This GUI wrapper is provided as-is for educational and personal use. Gallery-dl itself is licensed under GPL-2.0.

## Contributing

Feel free to submit issues and enhancement requests!

## Building Standalone Executables

You can create standalone executable files that users can run without installing Python or any dependencies.

### Quick Build

**Linux/macOS:**
```bash
./quick_build.sh
```

**Windows:**
```batch
quick_build.bat
```

**Manual build:**
```bash
# Install PyInstaller
pip install pyinstaller

# Build for current platform
python build_executable.py

# Build for specific platform
python build_executable.py --platform windows
python build_executable.py --platform linux  
python build_executable.py --platform macos
```

### GitHub Releases

The project includes GitHub Actions workflow for automatic builds:

1. **Tag a release:**
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

2. **Create GitHub release** - Go to GitHub → Releases → "Create a new release"

3. **Automatic builds** - The workflow will automatically build executables for all platforms

4. **Download executables** - Users can download and run without any installation

### File Sizes
- **Windows**: ~50-80 MB
- **Linux**: ~45-70 MB  
- **macOS**: ~55-85 MB

Large file sizes are normal for standalone executables as they include the Python runtime and all dependencies.

For detailed build instructions, see [BUILD_EXECUTABLE.md](BUILD_EXECUTABLE.md).

## Acknowledgments

- [gallery-dl](https://github.com/mikf/gallery-dl) by mikf - The powerful download engine that makes this possible
- Built with Python's tkinter for cross-platform compatibility
