"""
Download controller for managing gallery-dl downloads.
"""
import threading
import queue
import time
from typing import Callable, Optional, List
from models.settings import AppState
from utils.gallery_dl_service import GalleryDLService
from utils.file_utils import FileUtils


class DownloadController:
    """Controller for managing downloads."""
    
    def __init__(self, app_state: AppState, message_callback: Callable[[str, str], None]):
        self.app_state = app_state
        self.message_callback = message_callback  # Callback to send messages to UI
        self.message_queue = queue.Queue()
        
    def test_url(self) -> bool:
        """Test URL without downloading."""
        if self.app_state.is_testing:
            return False
            
        url = self.app_state.url_var.get().strip()
        if not url:
            self.message_callback("error", "Please enter a URL")
            return False
        
        # Start testing state
        self.app_state.is_testing = True
        self.message_callback("status", "Testing URL...")
        self.message_callback("log", f"Testing URL: {url}")
        
        def test_worker():
            try:
                success, message, output_lines = GalleryDLService.test_url(url)
                
                self.message_queue.put(("log", message))
                
                if success and output_lines:
                    self.message_queue.put(("log", "Sample output:"))
                    # Show first few lines of output
                    for line in output_lines[:5]:
                        self.message_queue.put(("log", f"  {line}"))
                    if len(output_lines) > 5:
                        self.message_queue.put(("log", f"  ... and {len(output_lines) - 5} more lines"))
                
                status = "URL test successful" if success else "URL test failed"
                self.message_queue.put(("status", status))
                
            except Exception as e:
                self.message_queue.put(("log", f"✗ Test error: {str(e)}"))
                self.message_queue.put(("status", "URL test error"))
            finally:
                self.message_queue.put(("test_finished", None))
        
        threading.Thread(target=test_worker, daemon=True).start()
        return True
    
    def start_download(self) -> bool:
        """Start download in separate thread."""
        if self.app_state.is_downloading:
            return False
        
        cmd = self.app_state.build_gallery_dl_command()
        if not cmd:
            self.message_callback("error", "Please enter a URL")
            return False
        
        # Add URL to history
        url = self.app_state.url_var.get().strip()
        self.app_state.add_url_to_history(url)
        
        # Ensure download directory exists
        download_path = self.app_state.download_path.get()
        if not FileUtils.ensure_directory_exists(download_path):
            self.message_callback("error", f"Cannot create download directory: {download_path}")
            return False
        
        self.app_state.is_downloading = True
        self.message_callback("status", "Downloading...")
        self.message_callback("download_started", None)
        
        # Start download thread
        download_thread = threading.Thread(target=self._download_worker, args=(cmd,))
        download_thread.daemon = True
        download_thread.start()
        return True
    
    def _download_worker(self, cmd: List[str]):
        """Download worker thread."""
        output_lines = []
        try:
            self.message_queue.put(("log", f"Starting download: {' '.join(cmd)}"))
            
            # Create download process
            self.app_state.download_process = GalleryDLService.create_download_process(cmd)
            
            # Read output and store for analysis
            for line in iter(self.app_state.download_process.stdout.readline, ''):
                if not self.app_state.is_downloading:
                    break
                line_stripped = line.strip()
                if line_stripped:
                    output_lines.append(line_stripped)
                    self.message_queue.put(("log", line_stripped))
            
            self.app_state.download_process.wait()
            
            if self.app_state.download_process.returncode == 0:
                self.message_queue.put(("status", "Download completed successfully"))
                self.message_queue.put(("log", "✓ Download completed"))
            else:
                exit_code = self.app_state.download_process.returncode
                error_desc = GalleryDLService.get_error_description(exit_code)
                
                # Analyze output for more specific error context
                error_context = GalleryDLService.analyze_error_output(output_lines, exit_code)
                
                self.message_queue.put(("status", "Download failed"))
                self.message_queue.put(("log", f"✗ Download failed (exit code: {exit_code})"))
                self.message_queue.put(("log", f"  Reason: {error_desc}"))
                if error_context:
                    self.message_queue.put(("log", f"  Context: {error_context}"))
                
        except Exception as e:
            self.message_queue.put(("status", "Download error"))
            self.message_queue.put(("log", f"✗ Error: {str(e)}"))
        finally:
            self.message_queue.put(("finished", None))
    
    def stop_download(self):
        """Stop current download."""
        if self.app_state.download_process and self.app_state.is_downloading:
            self.app_state.is_downloading = False
            try:
                self.app_state.download_process.terminate()
                self.message_callback("log", "Download stopped by user")
            except:
                pass
    
    def process_messages(self) -> bool:
        """Process messages from download thread. Returns True if messages were processed."""
        messages_processed = False
        try:
            while True:
                message_type, message = self.message_queue.get_nowait()
                messages_processed = True
                
                if message_type == "log":
                    self.message_callback("log", message)
                elif message_type == "status":
                    self.message_callback("status", message)
                elif message_type == "finished":
                    self._finish_download()
                elif message_type == "test_finished":
                    self._finish_test()
                    
        except queue.Empty:
            pass
        
        return messages_processed
    
    def _finish_download(self):
        """Clean up after download."""
        self.app_state.is_downloading = False
        self.app_state.download_process = None
        self.message_callback("download_finished", None)
    
    def _finish_test(self):
        """Clean up after URL test."""
        self.app_state.is_testing = False
        if not self.app_state.is_downloading:
            self.message_callback("status", "Ready")
        self.message_callback("test_finished", None)
