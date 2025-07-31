"""
File and system utilities for Gallery-DL GUI.
"""
import os
import sys
import subprocess
import webbrowser
from pathlib import Path
from typing import Optional


class FileUtils:
    """Utilities for file and folder operations."""
    
    @staticmethod
    def open_folder(path: str) -> bool:
        """Open folder in file explorer."""
        if not os.path.exists(path):
            return False
        
        try:
            if sys.platform == "win32":
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.run(["open", path])
            else:
                subprocess.run(["xdg-open", path])
            return True
        except Exception:
            return False
    
    @staticmethod
    def ensure_directory_exists(path: str) -> bool:
        """Ensure directory exists, create if it doesn't."""
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except OSError:
            return False
    
    @staticmethod
    def open_url(url: str) -> bool:
        """Open URL in default browser."""
        try:
            webbrowser.open(url)
            return True
        except Exception:
            return False


class ClipboardUtils:
    """Utilities for clipboard operations."""
    
    @staticmethod
    def get_clipboard_content(root) -> Optional[str]:
        """Get content from clipboard."""
        try:
            return root.clipboard_get()
        except Exception:
            return None
    
    @staticmethod
    def set_clipboard_content(root, content: str) -> bool:
        """Set clipboard content."""
        try:
            root.clipboard_clear()
            root.clipboard_append(content)
            return True
        except Exception:
            return False
