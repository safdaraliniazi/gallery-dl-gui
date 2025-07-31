"""
Real web browser widget for Gallery-DL GUI using tkinter and embedded browser.
"""
import tkinter as tk
from tkinter import ttk
import webbrowser
import threading
import os
import tempfile
import subprocess
import sys
from typing import Optional


class RealWebPreview:
    """Real web browser preview widget."""
    
    def __init__(self, parent, width: int = 600, height: int = 400):
        self.parent = parent
        self.current_url = ""
        self.temp_html_file = None
        
        # Create preview frame
        self.frame = ttk.LabelFrame(parent, text="Website Preview", padding="5")
        
        # Create toolbar
        self._create_toolbar()
        
        # Try to create browser widget
        self._create_browser_area(width, height)
        
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
    
    def _create_browser_area(self, width: int, height: int):
        """Create browser display area."""
        # Create container frame
        browser_frame = ttk.Frame(self.frame)
        browser_frame.pack(fill="both", expand=True)
        
        # Try to use tkinter HTML widget if available
        try:
            self._create_html_widget(browser_frame, width, height)
        except ImportError:
            # Fallback to embedded browser or iframe approach
            self._create_iframe_widget(browser_frame, width, height)
    
    def _create_html_widget(self, parent, width: int, height: int):
        """Create HTML widget using tkinter_html if available."""
        try:
            # Try to import tkinter_html
            from tkinter import html
            
            self.html_widget = html.HTMLText(parent, width=width//10, height=height//20)
            self.html_widget.pack(fill="both", expand=True)
            
            # Add scrollbars
            v_scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.html_widget.yview)
            self.html_widget.configure(yscrollcommand=v_scrollbar.set)
            v_scrollbar.pack(side="right", fill="y")
            
            self.browser_type = "html_widget"
            
        except ImportError:
            raise ImportError("HTML widget not available")
    
    def _create_iframe_widget(self, parent, width: int, height: int):
        """Create iframe-based browser widget."""
        # Create a frame for the browser
        self.browser_container = ttk.Frame(parent)
        self.browser_container.pack(fill="both", expand=True)
        
        # Create an embedded HTML viewer using temporary files
        self.html_display = tk.Text(self.browser_container, wrap=tk.NONE,
                                   width=width//10, height=height//20,
                                   font=("Courier", 9))
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(self.browser_container, orient="vertical", 
                                   command=self.html_display.yview)
        h_scrollbar = ttk.Scrollbar(self.browser_container, orient="horizontal", 
                                   command=self.html_display.xview)
        
        self.html_display.configure(yscrollcommand=v_scrollbar.set, 
                                   xscrollcommand=h_scrollbar.set)
        
        # Pack widgets
        self.html_display.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        self.browser_container.grid_rowconfigure(0, weight=1)
        self.browser_container.grid_columnconfigure(0, weight=1)
        
        self.browser_type = "text_widget"
        
        # Show default message
        self._show_iframe_message("Select a website from the list to preview it here.")
    
    def load_url(self, url: str, site_name: str = ""):
        """Load and display website."""
        if not url or url == self.current_url:
            return
            
        self.current_url = url
        self.url_var.set(f"{site_name}: {url}" if site_name else url)
        
        if self.browser_type == "html_widget":
            self._load_html_widget(url)
        else:
            self._load_iframe_widget(url, site_name)
    
    def _load_html_widget(self, url: str):
        """Load URL in HTML widget."""
        # Show loading message
        self.html_widget.delete(1.0, tk.END)
        self.html_widget.insert(tk.END, f"Loading {url}...")
        
        # Load content in background
        threading.Thread(target=self._fetch_html_content, args=(url,), daemon=True).start()
    
    def _load_iframe_widget(self, url: str, site_name: str):
        """Load URL using iframe approach."""
        # Create HTML with iframe
        html_content = self._create_iframe_html(url, site_name)
        
        # Create temporary HTML file
        self._create_temp_html_file(html_content)
        
        # Show the iframe HTML content in text widget
        self._show_iframe_content(html_content)
    
    def _create_iframe_html(self, url: str, site_name: str) -> str:
        """Create HTML content with iframe."""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>{site_name} Preview</title>
    <style>
        body {{
            margin: 0;
            padding: 10px;
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
        }}
        .header {{
            background-color: #333;
            color: white;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }}
        .iframe-container {{
            border: 2px solid #ddd;
            border-radius: 5px;
            overflow: hidden;
            background-color: white;
        }}
        iframe {{
            width: 100%;
            height: 500px;
            border: none;
        }}
        .info {{
            margin: 10px 0;
            padding: 10px;
            background-color: #e8f4f8;
            border-left: 4px solid #2196F3;
        }}
        .buttons {{
            margin: 10px 0;
        }}
        button {{
            background-color: #2196F3;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            margin-right: 10px;
        }}
        button:hover {{
            background-color: #1976D2;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h2>{site_name} - Website Preview</h2>
        <p>URL: <a href="{url}" target="_blank" style="color: #4CAF50;">{url}</a></p>
    </div>
    
    <div class="info">
        <strong>About this website:</strong><br>
        This is one of the 300+ websites supported by gallery-dl. You can download images and media from this site using the Gallery-DL GUI.
    </div>
    
    <div class="buttons">
        <button onclick="window.open('{url}', '_blank')">Open in New Tab</button>
        <button onclick="location.reload()">Refresh Preview</button>
    </div>
    
    <div class="iframe-container">
        <iframe src="{url}" 
                sandbox="allow-same-origin allow-scripts allow-popups allow-forms"
                loading="lazy">
            <p>Your browser does not support iframes. <a href="{url}">Click here to visit {site_name}</a></p>
        </iframe>
    </div>
    
    <div class="info">
        <strong>How to download from this site:</strong><br>
        1. Copy a URL from the website above<br>
        2. Go to the Download tab in Gallery-DL GUI<br>
        3. Paste the URL and configure your options<br>
        4. Click Download to start downloading
    </div>
</body>
</html>
"""
    
    def _create_temp_html_file(self, html_content: str):
        """Create temporary HTML file for preview."""
        try:
            # Clean up previous temp file
            if self.temp_html_file and os.path.exists(self.temp_html_file):
                os.unlink(self.temp_html_file)
            
            # Create new temp file
            fd, self.temp_html_file = tempfile.mkstemp(suffix='.html', prefix='gdlgui_preview_')
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                f.write(html_content)
        
        except Exception as e:
            print(f"Error creating temp HTML file: {e}")
    
    def _show_iframe_content(self, html_content: str):
        """Show HTML content in text widget and offer to open in browser."""
        self.html_display.config(state=tk.NORMAL)
        self.html_display.delete(1.0, tk.END)
        
        # Show a preview message with option to open in browser
        preview_text = f"""
🌐 WEBSITE PREVIEW

Current Site: {self.current_url}

📝 Note: For the best preview experience, click "Open Preview in Browser" below 
    to see the actual website in your default browser.

🔧 This preview shows:
• Website URL and basic information
• Instructions for downloading content
• Direct link to open the site

💡 Why use Gallery-DL GUI:
• Download entire galleries and collections
• Support for 300+ websites
• Batch downloads with progress tracking
• Configurable download options

📋 To download from this site:
1. Visit the website (click "Open in Browser" above)
2. Copy URLs of content you want to download
3. Go to the Download tab
4. Paste the URL and click Download

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Click "Open Preview in Browser" above to see the actual website!
"""
        
        self.html_display.insert(tk.END, preview_text)
        self.html_display.config(state=tk.DISABLED)
        
        # Add button to open HTML preview in browser
        if hasattr(self, 'preview_button'):
            self.preview_button.destroy()
        
        self.preview_button = ttk.Button(self.toolbar, text="Open Preview in Browser", 
                                        command=self._open_html_preview)
        self.preview_button.pack(side="right", padx=(5, 0))
    
    def _show_iframe_message(self, message: str):
        """Show a message in the iframe area."""
        self.html_display.config(state=tk.NORMAL)
        self.html_display.delete(1.0, tk.END)
        self.html_display.insert(tk.END, message)
        self.html_display.config(state=tk.DISABLED)
    
    def _fetch_html_content(self, url: str):
        """Fetch HTML content for display."""
        try:
            import urllib.request
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode('utf-8', errors='ignore')
                
            # Update HTML widget in main thread
            self.parent.after(0, lambda: self._update_html_widget(content))
            
        except Exception as e:
            error_msg = f"Error loading website: {str(e)}"
            self.parent.after(0, lambda: self._update_html_widget(error_msg))
    
    def _update_html_widget(self, content: str):
        """Update HTML widget content."""
        if hasattr(self, 'html_widget'):
            self.html_widget.delete(1.0, tk.END)
            self.html_widget.insert(tk.END, content)
    
    def _open_in_browser(self):
        """Open current URL in default browser."""
        if self.current_url:
            webbrowser.open(self.current_url)
    
    def _open_html_preview(self):
        """Open HTML preview in browser."""
        if self.temp_html_file and os.path.exists(self.temp_html_file):
            webbrowser.open(f"file://{self.temp_html_file}")
        elif self.current_url:
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
    
    def __del__(self):
        """Cleanup temporary files."""
        if self.temp_html_file and os.path.exists(self.temp_html_file):
            try:
                os.unlink(self.temp_html_file)
            except:
                pass
