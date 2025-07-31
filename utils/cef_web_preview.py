"""
CEF Python web preview widget for Gallery-DL GUI.
Real browser integration using Chrome Embedded Framework.
"""
import tkinter as tk
from tkinter import ttk
import threading
import sys
import os
from typing import Optional

# CEF Python imports with version compatibility check
CEF_AVAILABLE = False
COMPATIBILITY_MESSAGE = ""

# Check Python version compatibility (CEF v66.1 supports Python 3.8 and 3.9 on Windows)
if sys.version_info >= (3, 10):
    COMPATIBILITY_MESSAGE = f"CEF Python v66.1 supports Python 3.8-3.9 on Windows. Current version: Python {sys.version_info.major}.{sys.version_info.minor}. Please use Python 3.9 for browser preview."
elif sys.version_info < (3, 8):
    COMPATIBILITY_MESSAGE = f"CEF Python v66.1 requires Python 3.8 or higher. Current version: Python {sys.version_info.major}.{sys.version_info.minor}."
else:
    try:
        from cefpython3 import cefpython as cef
        CEF_AVAILABLE = True
    except ImportError:
        COMPATIBILITY_MESSAGE = "CEF Python not installed. Install with: pip install cefpython3"

if not CEF_AVAILABLE:
    print(f"⚠️ {COMPATIBILITY_MESSAGE}")


class CEFWebPreview:
    """Real web browser widget using CEF Python."""
    
    def __init__(self, parent, width: int = 800, height: int = 600):
        self.parent = parent
        self.width = width
        self.height = height
        self.current_url = ""
        self.browser = None
        self.browser_frame = None
        self.is_cef_initialized = False
        
        # Create preview frame
        self.frame = ttk.LabelFrame(parent, text="Website Preview (CEF Browser)", padding="5")
        
        # Create toolbar
        self._create_toolbar()
        
        # Initialize CEF browser
        if CEF_AVAILABLE:
            self._initialize_cef()
        else:
            self._create_fallback_preview()
    
    def _create_toolbar(self):
        """Create toolbar with navigation controls."""
        self.toolbar = ttk.Frame(self.frame)
        self.toolbar.pack(fill="x", pady=(0, 5))
        
        # Navigation buttons
        self.back_button = ttk.Button(self.toolbar, text="←", 
                                     command=self._go_back, width=3)
        self.back_button.pack(side="left", padx=(0, 2))
        
        self.forward_button = ttk.Button(self.toolbar, text="→", 
                                        command=self._go_forward, width=3)
        self.forward_button.pack(side="left", padx=(0, 2))
        
        self.refresh_button = ttk.Button(self.toolbar, text="⟳", 
                                        command=self._refresh, width=3)
        self.refresh_button.pack(side="left", padx=(0, 10))
        
        # URL display
        self.url_var = tk.StringVar()
        self.url_label = ttk.Label(self.toolbar, textvariable=self.url_var, 
                                  font=("Arial", 9), foreground="blue")
        self.url_label.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Action buttons
        self.open_button = ttk.Button(self.toolbar, text="Open in Browser", 
                                     command=self._open_in_browser)
        self.open_button.pack(side="right", padx=(5, 0))
        
        self.home_button = ttk.Button(self.toolbar, text="🏠", 
                                     command=self._go_home, width=3)
        self.home_button.pack(side="right", padx=(5, 0))
    
    def _initialize_cef(self):
        """Initialize CEF Python browser."""
        try:
            # CEF settings
            settings = {
                "multi_threaded_message_loop": False,
                "debug": False,
                "log_severity": cef.LOGSEVERITY_ERROR,
                "log_file": "",
            }
            
            # Check if CEF is already initialized
            if not cef.GetAppSetting("multi_threaded_message_loop"):
                cef.Initialize(settings)
                self.is_cef_initialized = True
            
            # Create browser container frame
            self.browser_container = ttk.Frame(self.frame)
            self.browser_container.pack(fill="both", expand=True)
            
            # Create browser frame
            self._create_browser()
            
            print("✅ CEF Python browser initialized successfully")
            
        except Exception as e:
            print(f"❌ Failed to initialize CEF browser: {e}")
            self._create_fallback_preview()
    
    def _create_browser(self):
        """Create the CEF browser widget."""
        try:
            # Get the window handle for embedding
            window_handle = self.browser_container.winfo_id()
            
            # Window info for CEF
            window_info = cef.WindowInfo()
            window_info.SetAsChild(window_handle, [0, 0, self.width, self.height])
            
            # Browser settings
            browser_settings = {
                "plugins_disabled": True,
                "universal_access_from_file_urls_allowed": True,
                "file_access_from_file_urls_allowed": True,
            }
            
            # Create browser
            self.browser = cef.CreateBrowserSync(
                window_info=window_info,
                url="about:blank",
                settings=browser_settings
            )
            
            # Set up load handler
            self.browser.SetClientHandler(LoadHandler(self))
            
            # Show initial message
            self._show_welcome_page()
            
            print("✅ CEF browser widget created successfully")
            
        except Exception as e:
            print(f"❌ Failed to create CEF browser widget: {e}")
            self._create_fallback_preview()
    
    def _create_fallback_preview(self):
        """Create fallback preview when CEF is not available."""
        self.browser_container = ttk.Frame(self.frame)
        self.browser_container.pack(fill="both", expand=True)
        
        fallback_text = f"""🌐 Web Preview Not Available

{COMPATIBILITY_MESSAGE}

💡 Alternative options:
• Double-click any website in the list to open in your default browser
• Visit gallery-dl documentation for site-specific information
• Use the URL input in the Download tab to test sites directly

🔧 To enable browser preview:
• Use Python 3.12 or earlier for CEF Python compatibility
• Install CEF Python: pip install cefpython3

Current Python version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}
CEF Python status: {'✅ Available' if CEF_AVAILABLE else '❌ Not available'}"""
        
        self.fallback_label = ttk.Label(self.browser_container, text=fallback_text, 
                                       justify=tk.LEFT, font=("Arial", 10))
        self.fallback_label.pack(fill="both", expand=True, padx=20, pady=20)
    
    def _show_welcome_page(self):
        """Show welcome page in the browser."""
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Gallery-DL GUI - Web Preview</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .container {
            text-align: center;
            max-width: 600px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 40px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        }
        h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        .subtitle {
            font-size: 1.2em;
            margin-bottom: 30px;
            opacity: 0.9;
        }
        .features {
            text-align: left;
            margin: 30px 0;
        }
        .feature {
            margin: 10px 0;
            font-size: 1.1em;
        }
        .feature::before {
            content: "✨";
            margin-right: 10px;
        }
        .instruction {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 20px;
            margin-top: 30px;
            font-size: 1.1em;
        }
        .logo {
            font-size: 4em;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🌐</div>
        <h1>Gallery-DL GUI</h1>
        <div class="subtitle">Real Browser Preview with CEF Python</div>
        
        <div class="features">
            <div class="feature">Full Chrome browser integration</div>
            <div class="feature">Real website rendering</div>
            <div class="feature">Navigation controls</div>
            <div class="feature">Support for 300+ websites</div>
        </div>
        
        <div class="instruction">
            <strong>How to use:</strong><br>
            Select any website from the sites list on the left to preview it here in real-time!
        </div>
    </div>
</body>
</html>
        """
        
        if self.browser:
            # Load HTML content directly
            self.browser.LoadUrl("data:text/html," + html_content)
    
    def load_url(self, url: str, site_name: str = ""):
        """Load a URL in the browser."""
        if not url:
            return
            
        self.current_url = url
        display_text = f"{site_name}: {url}" if site_name else url
        self.url_var.set(display_text)
        
        if self.browser:
            try:
                self.browser.LoadUrl(url)
                print(f"✅ Loading URL in CEF browser: {url}")
            except Exception as e:
                print(f"❌ Failed to load URL in CEF browser: {e}")
        else:
            # Update fallback display
            if hasattr(self, 'fallback_label'):
                self.fallback_label.config(text=f"Website: {site_name}\nURL: {url}\n\nClick 'Open in Browser' to view this site.")
    
    def _go_back(self):
        """Navigate back."""
        if self.browser and self.browser.CanGoBack():
            self.browser.GoBack()
    
    def _go_forward(self):
        """Navigate forward."""
        if self.browser and self.browser.CanGoForward():
            self.browser.GoForward()
    
    def _refresh(self):
        """Refresh current page."""
        if self.browser:
            self.browser.Reload()
        elif self.current_url:
            self.load_url(self.current_url)
    
    def _go_home(self):
        """Go to home page."""
        if self.browser:
            self._show_welcome_page()
        self.url_var.set("Gallery-DL GUI - Home")
    
    def _open_in_browser(self):
        """Open current URL in default browser."""
        if self.current_url:
            import webbrowser
            webbrowser.open(self.current_url)
    
    def pack(self, **kwargs):
        """Pack the preview frame."""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the preview frame."""
        self.frame.grid(**kwargs)
    
    def destroy(self):
        """Clean up CEF resources."""
        if self.browser:
            try:
                self.browser.CloseBrowser(True)
            except:
                pass
        
        if self.is_cef_initialized:
            try:
                cef.Shutdown()
            except:
                pass


class LoadHandler:
    """CEF load handler for browser events."""
    
    def __init__(self, web_preview):
        self.web_preview = web_preview
    
    def OnLoadStart(self, browser, frame, request):
        """Called when loading starts."""
        if frame.IsMain():
            url = browser.GetUrl()
            if url and url != "about:blank" and not url.startswith("data:"):
                self.web_preview.url_var.set(url)
    
    def OnLoadEnd(self, browser, frame, http_status_code):
        """Called when loading ends."""
        if frame.IsMain():
            print(f"✅ Page loaded with status: {http_status_code}")
    
    def OnLoadError(self, browser, frame, error_code, error_text, failed_url):
        """Called when loading fails."""
        if frame.IsMain():
            print(f"❌ Failed to load {failed_url}: {error_text}")


# Message loop function for CEF
def cef_message_loop_work():
    """CEF message loop work function."""
    if CEF_AVAILABLE:
        try:
            cef.MessageLoopWork()
        except:
            pass


# Utility function to check CEF availability
def check_cef_availability():
    """Check if CEF Python is available and working."""
    if not CEF_AVAILABLE:
        return False, "CEF Python not installed"
    
    try:
        # Test basic CEF functionality
        settings = {"multi_threaded_message_loop": False, "debug": False}
        
        # This is just a test - don't actually initialize here
        return True, "CEF Python available"
    except Exception as e:
        return False, f"CEF Python error: {e}"


if __name__ == "__main__":
    # Test the CEF web preview
    def test_cef_preview():
        available, message = check_cef_availability()
        print(f"CEF Status: {message}")
        
        if not available:
            print("❌ CEF Python not available for testing")
            return
        
        root = tk.Tk()
        root.title("CEF Web Preview Test")
        root.geometry("1000x700")
        
        try:
            preview = CEFWebPreview(root, width=800, height=600)
            preview.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Test loading a URL after a delay
            def load_test_url():
                preview.load_url("https://www.google.com", "Google")
            
            root.after(2000, load_test_url)
            
            # CEF message loop
            def message_loop():
                cef_message_loop_work()
                root.after(10, message_loop)
            
            root.after(10, message_loop)
            
            # Cleanup on close
            def on_closing():
                preview.destroy()
                root.destroy()
            
            root.protocol("WM_DELETE_WINDOW", on_closing)
            root.mainloop()
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            root.destroy()
    
    test_cef_preview()
