"""
Configuration and settings management for Gallery-DL GUI.
"""
import json
import tkinter as tk
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class GalleryDLSettings:
    """Data class for Gallery-DL settings."""
    download_path: str = ""
    username: str = ""
    cookies_file: str = ""
    config_file: str = ""
    url_history: List[str] = None
    extract_links: bool = False
    no_download: bool = False
    write_info: bool = False
    write_metadata: bool = False
    
    def __post_init__(self):
        if self.url_history is None:
            self.url_history = []
        if not self.download_path:
            self.download_path = str(Path.home() / "Downloads" / "gallery-dl")


class SettingsManager:
    """Manages application settings persistence."""
    
    SETTINGS_FILE = Path.home() / ".gallery-dl-gui-settings.json"
    
    @classmethod
    def save_settings(cls, settings: GalleryDLSettings) -> bool:
        """Save settings to file."""
        try:
            settings_dict = asdict(settings)
            with open(cls.SETTINGS_FILE, 'w') as f:
                json.dump(settings_dict, f, indent=2)
            return True
        except Exception as e:
            print(f"Failed to save settings: {e}")
            return False
    
    @classmethod
    def load_settings(cls) -> GalleryDLSettings:
        """Load settings from file."""
        try:
            if cls.SETTINGS_FILE.exists():
                with open(cls.SETTINGS_FILE, 'r') as f:
                    settings_dict = json.load(f)
                return GalleryDLSettings(**settings_dict)
        except Exception as e:
            print(f"Failed to load settings: {e}")
        
        return GalleryDLSettings()


class AppState:
    """Manages application state."""
    
    def __init__(self):
        # Tkinter variables
        self.download_path = tk.StringVar()
        self.url_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")
        self.progress_var = tk.DoubleVar()
        
        # Advanced options
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.cookies_file_var = tk.StringVar()
        self.config_file_var = tk.StringVar()
        
        # Download options
        self.extract_links_var = tk.BooleanVar()
        self.no_download_var = tk.BooleanVar()
        self.write_info_var = tk.BooleanVar()
        self.write_metadata_var = tk.BooleanVar()
        
        # Search variables for sites list
        self.search_var = tk.StringVar()
        self.category_var = tk.StringVar(value="All")
        
        # Application state
        self.url_history: List[str] = []
        self.is_downloading = False
        self.is_testing = False
        self.download_process = None
        
        # Load settings
        self.load_settings()
    
    def load_settings(self):
        """Load settings and update variables."""
        settings = SettingsManager.load_settings()
        
        self.download_path.set(settings.download_path)
        self.username_var.set(settings.username)
        self.cookies_file_var.set(settings.cookies_file)
        self.config_file_var.set(settings.config_file)
        self.url_history = settings.url_history
        
        self.extract_links_var.set(settings.extract_links)
        self.no_download_var.set(settings.no_download)
        self.write_info_var.set(settings.write_info)
        self.write_metadata_var.set(settings.write_metadata)
    
    def save_settings(self) -> bool:
        """Save current state to settings."""
        settings = GalleryDLSettings(
            download_path=self.download_path.get(),
            username=self.username_var.get(),
            cookies_file=self.cookies_file_var.get(),
            config_file=self.config_file_var.get(),
            url_history=self.url_history,
            extract_links=self.extract_links_var.get(),
            no_download=self.no_download_var.get(),
            write_info=self.write_info_var.get(),
            write_metadata=self.write_metadata_var.get()
        )
        
        return SettingsManager.save_settings(settings)
    
    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        settings = GalleryDLSettings()
        
        self.download_path.set(settings.download_path)
        self.username_var.set("")
        self.password_var.set("")
        self.cookies_file_var.set("")
        self.config_file_var.set("")
        self.url_history = []
        self.url_var.set("")
        
        self.extract_links_var.set(False)
        self.no_download_var.set(False)
        self.write_info_var.set(False)
        self.write_metadata_var.set(False)
    
    def build_gallery_dl_command(self) -> Optional[List[str]]:
        """Build gallery-dl command based on current settings."""
        url = self.url_var.get().strip()
        if not url:
            return None
        
        cmd = ["gallery-dl"]
        
        # Add authentication
        if self.username_var.get():
            cmd.extend(["-u", self.username_var.get()])
        if self.password_var.get():
            cmd.extend(["-p", self.password_var.get()])
        
        # Add cookies
        if self.cookies_file_var.get():
            cmd.extend(["--cookies", self.cookies_file_var.get()])
        
        # Add config
        if self.config_file_var.get():
            cmd.extend(["--config", self.config_file_var.get()])
        
        # Add options
        if self.extract_links_var.get():
            cmd.append("-g")
        if self.no_download_var.get():
            cmd.append("--no-download")
        if self.write_info_var.get():
            cmd.append("--write-info-json")
        if self.write_metadata_var.get():
            cmd.append("--write-metadata")
        
        # Add download path
        download_path = self.download_path.get().strip()
        if download_path:
            cmd.extend(["-d", download_path])
        
        # Add URL
        cmd.append(url)
        
        return cmd
    
    def add_url_to_history(self, url: str):
        """Add URL to history if not already present."""
        if url and url not in self.url_history:
            self.url_history.append(url)
