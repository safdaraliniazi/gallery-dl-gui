"""
Main download tab view for Gallery-DL GUI.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import Callable, Optional
from views.base_view import BaseTab
from models.settings import AppState
from utils.file_utils import ClipboardUtils, FileUtils


class DownloadTab(BaseTab):
    """Main download tab with URL input, settings, and progress display."""
    
    def __init__(self, notebook: ttk.Notebook, app_state: AppState, callbacks: dict):
        self.app_state = app_state
        self.callbacks = callbacks
        super().__init__(notebook, "Download")
    
    def setup_tab(self):
        """Setup the download tab content."""
        # Configure grid weights
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(5, weight=1)  # Log area expands
        
        self._create_title()
        self._create_url_section()
        self._create_settings_section()
        self._create_control_buttons()
        self._create_progress_section()
        self._create_log_section()
    
    def _create_title(self):
        """Create the title label."""
        title_label = ttk.Label(self.frame, text="Gallery-DL GUI", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(10, 20))
    
    def _create_url_section(self):
        """Create URL input section."""
        url_frame = ttk.LabelFrame(self.frame, text="URL to Download", padding="10")
        url_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=10, pady=(0, 10))
        url_frame.columnconfigure(0, weight=1)
        
        # URL history dropdown
        self.url_combo = ttk.Combobox(url_frame, textvariable=self.app_state.url_var, font=("Arial", 10))
        self.url_combo.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        # URL buttons
        url_buttons_frame = ttk.Frame(url_frame)
        url_buttons_frame.grid(row=0, column=1)
        
        paste_btn = ttk.Button(url_buttons_frame, text="Paste", command=self._paste_url)
        paste_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.test_btn = ttk.Button(url_buttons_frame, text="Test URL", command=self._test_url)
        self.test_btn.pack(side=tk.LEFT)
    
    def _create_settings_section(self):
        """Create download settings section."""
        settings_frame = ttk.LabelFrame(self.frame, text="Download Settings", padding="10")
        settings_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=10, pady=(0, 10))
        settings_frame.columnconfigure(1, weight=1)
        
        # Download path
        ttk.Label(settings_frame, text="Download Path:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        path_frame = ttk.Frame(settings_frame)
        path_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        path_frame.columnconfigure(0, weight=1)
        
        self.path_entry = ttk.Entry(path_frame, textvariable=self.app_state.download_path)
        self.path_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        browse_btn = ttk.Button(path_frame, text="Browse", command=self._browse_folder)
        browse_btn.grid(row=0, column=1)
        
        # Options checkboxes
        options_frame = ttk.Frame(settings_frame)
        options_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Checkbutton(options_frame, text="Extract URLs only", 
                       variable=self.app_state.extract_links_var).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="No download (test)", 
                       variable=self.app_state.no_download_var).grid(row=0, column=1, sticky=tk.W, padx=(20, 0))
        ttk.Checkbutton(options_frame, text="Write info JSON", 
                       variable=self.app_state.write_info_var).grid(row=1, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="Write metadata", 
                       variable=self.app_state.write_metadata_var).grid(row=1, column=1, sticky=tk.W, padx=(20, 0))
    
    def _create_control_buttons(self):
        """Create control buttons."""
        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=3, column=0, pady=(0, 10))
        
        self.download_btn = ttk.Button(button_frame, text="Download", 
                                     command=self._start_download, style="Accent.TButton")
        self.download_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(button_frame, text="Stop", 
                                 command=self._stop_download, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = ttk.Button(button_frame, text="Clear Log", command=self._clear_log)
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        open_folder_btn = ttk.Button(button_frame, text="Open Folder", command=self._open_folder)
        open_folder_btn.pack(side=tk.LEFT)
    
    def _create_progress_section(self):
        """Create progress and status section."""
        progress_frame = ttk.Frame(self.frame)
        progress_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), padx=10, pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.status_label = ttk.Label(progress_frame, textvariable=self.app_state.status_var)
        self.status_label.grid(row=0, column=1)
    
    def _create_log_section(self):
        """Create log output section."""
        log_frame = ttk.LabelFrame(self.frame, text="Output Log", padding="5")
        log_frame.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, state=tk.DISABLED)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def _paste_url(self):
        """Paste URL from clipboard."""
        content = ClipboardUtils.get_clipboard_content(self.frame)
        if content:
            self.app_state.url_var.set(content)
    
    def _test_url(self):
        """Test URL without downloading."""
        if 'test_url' in self.callbacks:
            self.callbacks['test_url']()
    
    def _browse_folder(self):
        """Browse for download folder."""
        if 'browse_folder' in self.callbacks:
            self.callbacks['browse_folder']()
    
    def _start_download(self):
        """Start download."""
        if 'start_download' in self.callbacks:
            self.callbacks['start_download']()
    
    def _stop_download(self):
        """Stop download."""
        if 'stop_download' in self.callbacks:
            self.callbacks['stop_download']()
    
    def _clear_log(self):
        """Clear the log."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def _open_folder(self):
        """Open download folder."""
        path = self.app_state.download_path.get()
        FileUtils.open_folder(path)
    
    def update_url_history(self):
        """Update URL combo values with history."""
        self.url_combo['values'] = self.app_state.url_history
    
    def log_message(self, message: str):
        """Add message to log with timestamp."""
        import time
        timestamp = time.strftime('%H:%M:%S')
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)
    
    def set_download_state(self, downloading: bool):
        """Update UI based on download state."""
        if downloading:
            self.download_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.progress_bar.start(10)
        else:
            self.download_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.progress_bar.stop()
    
    def set_test_state(self, testing: bool):
        """Update UI based on test state."""
        if testing:
            self.test_btn.config(state=tk.DISABLED, text="Testing...")
        else:
            self.test_btn.config(state=tk.NORMAL, text="Test URL")
