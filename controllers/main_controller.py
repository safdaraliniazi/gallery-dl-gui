"""
Main application controller for Gallery-DL GUI.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from models.settings import AppState
from controllers.download_controller import DownloadController
from views.download_tab import DownloadTab
from views.advanced_tab import AdvancedTab
from views.about_tab import AboutTab
from utils.gallery_dl_service import GalleryDLService
from utils.file_utils import FileUtils


class MainController:
    """Main application controller following MVC pattern."""
    
    def __init__(self, root):
        self.root = root
        self.app_state = AppState()
        
        # Initialize download controller
        self.download_controller = DownloadController(
            self.app_state, 
            self._handle_message
        )
        
        # Setup UI
        self._setup_window()
        self._create_views()
        self._check_gallery_dl()
        self._start_message_processing()
    
    def _setup_window(self):
        """Setup main window properties."""
        self.root.title("Gallery-DL GUI")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # Set window to be resizable and start maximized if preferred
        self.root.resizable(True, True)
        
        # Try to maximize the window on startup
        try:
            self.root.state('zoomed')  # Windows
        except tk.TclError:
            try:
                self.root.attributes('-zoomed', True)  # Linux
            except tk.TclError:
                pass  # macOS or if maximizing fails
        
        # Bind cleanup to window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Set up the style
        self.style = ttk.Style()
        self.style.theme_use('clam')
    
    def _create_views(self):
        """Create and setup all views."""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Setup callback dictionary
        callbacks = {
            'test_url': self._test_url,
            'browse_folder': self._browse_folder,
            'start_download': self._start_download,
            'stop_download': self._stop_download,
            'save_settings': self._save_settings,
            'reset_settings': self._reset_settings
        }
        
        # Create tabs
        self.download_tab = DownloadTab(self.notebook, self.app_state, callbacks)
        self.advanced_tab = AdvancedTab(self.notebook, self.app_state, callbacks)
        self.about_tab = AboutTab(self.notebook, self.app_state)
        
        # Initialize URL history
        self.download_tab.update_url_history()
    
    def _check_gallery_dl(self):
        """Check if gallery-dl is installed."""
        success, message = GalleryDLService.check_installation()
        
        if success:
            self.download_tab.log_message(f"✓ {message}")
        else:
            self.download_tab.log_message(f"⚠ {message}")
    
    def _start_message_processing(self):
        """Start processing messages from background threads."""
        self._process_messages()
    
    def _process_messages(self):
        """Process messages from download controller."""
        self.download_controller.process_messages()
        
        # Schedule next check
        self.root.after(100, self._process_messages)
    
    def _handle_message(self, message_type: str, message: str):
        """Handle messages from controllers."""
        if message_type == "log":
            self.download_tab.log_message(message)
        elif message_type == "status":
            self.app_state.status_var.set(message)
        elif message_type == "error":
            messagebox.showerror("Error", message)
        elif message_type == "download_started":
            self.download_tab.set_download_state(True)
        elif message_type == "download_finished":
            self.download_tab.set_download_state(False)
            self.download_tab.update_url_history()
        elif message_type == "test_finished":
            self.download_tab.set_test_state(False)
    
    def _test_url(self):
        """Test URL without downloading."""
        self.download_tab.set_test_state(True)
        self.download_controller.test_url()
    
    def _browse_folder(self):
        """Browse for download folder."""
        folder = filedialog.askdirectory(initialdir=self.app_state.download_path.get())
        if folder:
            self.app_state.download_path.set(folder)
    
    def _start_download(self):
        """Start download process."""
        self.download_controller.start_download()
    
    def _stop_download(self):
        """Stop current download."""
        self.download_controller.stop_download()
    
    def _save_settings(self):
        """Save current settings."""
        success = self.app_state.save_settings()
        if success:
            self.download_tab.log_message("Settings saved")
            messagebox.showinfo("Settings", "Settings saved successfully")
        else:
            messagebox.showerror("Error", "Failed to save settings")
    
    def _reset_settings(self):
        """Reset settings to defaults."""
        if messagebox.askyesno("Reset Settings", 
                              "Are you sure you want to reset all settings to defaults?"):
            self.app_state.reset_to_defaults()
            self.download_tab.update_url_history()
            self.download_tab.log_message("Settings reset to defaults")
    
    def _on_closing(self):
        """Handle application closing with proper cleanup."""
        try:
            # Cleanup CEF resources if available
            if hasattr(self, 'about_tab') and hasattr(self.about_tab, 'cleanup'):
                self.about_tab.cleanup()
            
            # Stop any running downloads
            if hasattr(self, 'download_controller') and self.download_controller:
                self.download_controller.stop_download()
            
        except Exception as e:
            print(f"Error during cleanup: {e}")
        finally:
            # Close the application
            self.root.quit()
            self.root.destroy()


def main():
    """Main entry point."""
    root = tk.Tk()
    app = MainController(root)
    root.mainloop()


if __name__ == "__main__":
    main()
