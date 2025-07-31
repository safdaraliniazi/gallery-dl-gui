"""
Web preview widget for Gallery-DL GUI.
"""
import tkinter as tk
from tkinter import ttk
import webbrowser
import threading
import urllib.request
from urllib.parse import urlparse
from typing import Optional


class WebPreview:
    """Simple web preview widget using tkinter Text widget."""
    
    def __init__(self, parent, width: int = 600, height: int = 400):
        self.parent = parent
        self.current_url = ""
        
        # Create preview frame
        self.frame = ttk.LabelFrame(parent, text="Website Preview", padding="5")
        
        # Create toolbar
        self._create_toolbar()
        
        # Create content area
        self._create_content_area(width, height)
        
    def _create_toolbar(self):
        """Create toolbar with URL display and actions."""
        self.toolbar = ttk.Frame(self.frame)
        self.toolbar.pack(fill="x", pady=(0, 5))
        
        # URL label
        self.url_var = tk.StringVar()
        self.url_label = ttk.Label(self.toolbar, textvariable=self.url_var, 
                                  font=("Arial", 9), foreground="blue")
        self.url_label.pack(side="left", fill="x", expand=True)
        
        # Open in browser button
        self.open_button = ttk.Button(self.toolbar, text="Open in Browser", 
                                     command=self._open_in_browser)
        self.open_button.pack(side="right", padx=(5, 0))
        
        # Refresh button
        self.refresh_button = ttk.Button(self.toolbar, text="Refresh", 
                                        command=self._refresh_preview)
        self.refresh_button.pack(side="right", padx=(5, 0))
    
    def _create_content_area(self, width: int, height: int):
        """Create content display area."""
        # Create scrollable text area
        content_frame = ttk.Frame(self.frame)
        content_frame.pack(fill="both", expand=True)
        
        # Text widget for content
        self.text_area = tk.Text(content_frame, wrap=tk.WORD, 
                                width=width//10, height=height//20,
                                font=("Arial", 9), state=tk.DISABLED)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(content_frame, orient="vertical", 
                                   command=self.text_area.yview)
        h_scrollbar = ttk.Scrollbar(content_frame, orient="horizontal", 
                                   command=self.text_area.xview)
        
        self.text_area.configure(yscrollcommand=v_scrollbar.set, 
                               xscrollcommand=h_scrollbar.set)
        
        # Pack widgets
        self.text_area.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Default message
        self._show_message("Select a website from the list to preview it here.")
    
    def load_url(self, url: str, site_name: str = ""):
        """Load and display website information."""
        if not url or url == self.current_url:
            return
            
        self.current_url = url
        self.url_var.set(f"{site_name}: {url}" if site_name else url)
        
        # Show loading message
        self._show_message("Loading website information...")
        
        # Load content in background thread
        threading.Thread(target=self._load_content_async, 
                        args=(url, site_name), daemon=True).start()
    
    def _load_content_async(self, url: str, site_name: str):
        """Load website content asynchronously."""
        try:
            # Parse URL to get basic info
            parsed = urlparse(url)
            domain = parsed.netloc or parsed.path
            
            # Create website information
            content = self._create_website_info(url, site_name, domain)
            
            # Try to get basic page info (title, etc.)
            try:
                page_info = self._get_page_info(url)
                content += "\n" + page_info
            except Exception as e:
                content += f"\n\nNote: Could not fetch additional page information.\nReason: {str(e)}"
            
            # Update UI in main thread
            self.parent.after(0, lambda: self._show_content(content))
            
        except Exception as e:
            error_msg = f"Error loading website information:\n{str(e)}"
            self.parent.after(0, lambda: self._show_message(error_msg))
    
    def _create_website_info(self, url: str, site_name: str, domain: str) -> str:
        """Create basic website information."""
        info = []
        
        if site_name:
            info.append(f"Website: {site_name}")
        
        info.append(f"URL: {url}")
        info.append(f"Domain: {domain}")
        
        # Add some helpful information
        info.append("\n" + "="*50)
        info.append("About this website:")
        info.append("This is one of the websites supported by gallery-dl.")
        info.append("You can use gallery-dl to download images and media from this site.")
        info.append("\nTo download content:")
        info.append("1. Copy a URL from this website")
        info.append("2. Paste it in the Download tab")
        info.append("3. Configure your download options")
        info.append("4. Click Download")
        
        return "\n".join(info)
    
    def _get_page_info(self, url: str) -> str:
        """Get basic page information like title."""
        try:
            # Set a timeout and user agent
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                # Read first 2KB to look for title
                content = response.read(2048).decode('utf-8', errors='ignore')
                
                # Extract title
                title_start = content.lower().find('<title>')
                if title_start != -1:
                    title_start += 7
                    title_end = content.lower().find('</title>', title_start)
                    if title_end != -1:
                        title = content[title_start:title_end].strip()
                        return f"\nPage Title: {title}"
                
                return "\nPage information loaded successfully."
                
        except Exception as e:
            raise Exception(f"Failed to fetch page info: {str(e)}")
    
    def _show_content(self, content: str):
        """Display content in the text area."""
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, content)
        self.text_area.config(state=tk.DISABLED)
    
    def _show_message(self, message: str):
        """Show a simple message."""
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, message)
        self.text_area.config(state=tk.DISABLED)
    
    def _open_in_browser(self):
        """Open current URL in default browser."""
        if self.current_url:
            webbrowser.open(self.current_url)
    
    def _refresh_preview(self):
        """Refresh the current preview."""
        if self.current_url:
            url = self.current_url
            self.current_url = ""  # Force refresh
            site_name = self.url_var.get().split(": ")[0] if ": " in self.url_var.get() else ""
            self.load_url(url, site_name)
    
    def pack(self, **kwargs):
        """Pack the preview frame."""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the preview frame."""
        self.frame.grid(**kwargs)
