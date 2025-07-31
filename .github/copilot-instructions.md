<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Gallery-DL GUI Project Instructions

This is a Python GUI application that provides a user-friendly interface for gallery-dl, a command-line tool for downloading images from various websites.

## Project Context
- **Main application**: `gallery_dl_gui.py` - tkinter-based GUI wrapper for gallery-dl
- **Purpose**: Make gallery-dl accessible to users who prefer graphical interfaces
- **Target platforms**: Cross-platform (Windows, macOS, Linux)
- **GUI framework**: tkinter (built into Python)

## Code Style Guidelines
- Follow PEP 8 Python style guidelines
- Use descriptive variable and function names
- Add docstrings for all functions and classes
- Handle exceptions gracefully with user-friendly error messages
- Use threading for long-running operations to keep GUI responsive

## Key Features to Maintain
- Real-time output logging from gallery-dl subprocess
- Progress indication during downloads
- Thread-safe communication between GUI and download threads
- Automatic detection of gallery-dl installation
- Support for common gallery-dl options and flags

## Development Priorities
1. **User Experience**: Keep the interface intuitive and responsive
2. **Error Handling**: Provide clear feedback for common issues
3. **Cross-platform compatibility**: Ensure code works on all major platforms
4. **Performance**: Use threading to prevent GUI freezing during downloads

## When Adding Features
- Always test with both `gallery-dl` command and `python -m gallery_dl` fallback
- Add appropriate error handling and user feedback
- Update the README.md if adding new functionality
- Consider backward compatibility with different gallery-dl versions

## Testing Considerations
- Test with various URL types and sites
- Verify error handling with invalid URLs
- Test download cancellation functionality
- Check behavior when gallery-dl is not installed
