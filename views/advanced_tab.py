"""
Advanced settings tab view for Gallery-DL GUI.
"""
import tkinter as tk
from tkinter import ttk, filedialog
from views.base_view import BaseTab
from models.settings import AppState
from utils.file_utils import FileUtils


class AdvancedTab(BaseTab):
    """Advanced settings tab with authentication and configuration options."""
    
    def __init__(self, notebook: ttk.Notebook, app_state: AppState, callbacks: dict):
        self.app_state = app_state
        self.callbacks = callbacks
        super().__init__(notebook, "Advanced")
    
    def setup_tab(self):
        """Setup the advanced tab content."""
        self.frame.columnconfigure(0, weight=1)
        
        self._create_authentication_section()
        self._create_cookies_section()
        self._create_configuration_section()
        self._create_quick_actions()
    
    def _create_authentication_section(self):
        """Create authentication section."""
        auth_frame = ttk.LabelFrame(self.frame, text="Authentication", padding="10")
        auth_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=10, pady=10)
        auth_frame.columnconfigure(1, weight=1)
        
        ttk.Label(auth_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        ttk.Entry(auth_frame, textvariable=self.app_state.username_var).grid(
            row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(auth_frame, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        ttk.Entry(auth_frame, textvariable=self.app_state.password_var, show="*").grid(
            row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
    
    def _create_cookies_section(self):
        """Create cookies file section."""
        cookies_frame = ttk.LabelFrame(self.frame, text="Cookies", padding="10")
        cookies_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=10, pady=(0, 10))
        cookies_frame.columnconfigure(1, weight=1)
        
        ttk.Label(cookies_frame, text="Cookies file:").grid(row=0, column=0, sticky=tk.W)
        cookies_path_frame = ttk.Frame(cookies_frame)
        cookies_path_frame.grid(row=0, column=1, sticky=(tk.W, tk.E))
        cookies_path_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(cookies_path_frame, textvariable=self.app_state.cookies_file_var).grid(
            row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(cookies_path_frame, text="Browse", command=self._browse_cookies_file).grid(
            row=0, column=1)
    
    def _create_configuration_section(self):
        """Create configuration file section."""
        config_frame = ttk.LabelFrame(self.frame, text="Configuration", padding="10")
        config_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=10, pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)
        
        ttk.Label(config_frame, text="Config file:").grid(row=0, column=0, sticky=tk.W)
        config_path_frame = ttk.Frame(config_frame)
        config_path_frame.grid(row=0, column=1, sticky=(tk.W, tk.E))
        config_path_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(config_path_frame, textvariable=self.app_state.config_file_var).grid(
            row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(config_path_frame, text="Browse", command=self._browse_config_file).grid(
            row=0, column=1)
    
    def _create_quick_actions(self):
        """Create quick actions section."""
        actions_frame = ttk.LabelFrame(self.frame, text="Quick Actions", padding="10")
        actions_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), padx=10, pady=(0, 10))
        
        ttk.Button(actions_frame, text="Open gallery-dl documentation", 
                  command=self._open_docs).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(actions_frame, text="Save current settings", 
                  command=self._save_settings).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(actions_frame, text="Reset settings", 
                  command=self._reset_settings).pack(side=tk.LEFT)
    
    def _browse_cookies_file(self):
        """Browse for cookies file."""
        file_path = filedialog.askopenfilename(
            title="Select cookies file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.app_state.cookies_file_var.set(file_path)
    
    def _browse_config_file(self):
        """Browse for config file."""
        file_path = filedialog.askopenfilename(
            title="Select config file",
            filetypes=[("Config files", "*.conf"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            self.app_state.config_file_var.set(file_path)
    
    def _open_docs(self):
        """Open gallery-dl documentation."""
        FileUtils.open_url("https://gdl-org.github.io/docs/")
    
    def _save_settings(self):
        """Save current settings."""
        if 'save_settings' in self.callbacks:
            self.callbacks['save_settings']()
    
    def _reset_settings(self):
        """Reset settings to defaults."""
        if 'reset_settings' in self.callbacks:
            self.callbacks['reset_settings']()
