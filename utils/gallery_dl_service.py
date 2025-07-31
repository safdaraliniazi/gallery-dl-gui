"""
Gallery-DL service for handling downloads and URL testing.
"""
import subprocess
import sys
from typing import Optional, List, Tuple
from urllib.parse import urlparse


class GalleryDLService:
    """Service for interacting with gallery-dl."""
    
    ERROR_DESCRIPTIONS = {
        1: "General error or exception occurred",
        2: "Interrupted by user (Ctrl+C)",
        3: "Invalid command line arguments",
        4: "Input/output error (network issues, file permissions, or unsupported URL)",
        5: "Configuration error (invalid config file or settings)", 
        6: "Authentication error (invalid credentials or login required)",
        8: "Format or extraction error (unsupported site or changed website structure)",
        16: "File system error (disk full, permission denied, or path issues)",
        32: "Download error (corrupted files or incomplete downloads)",
        64: "Unsupported URL or site - gallery-dl cannot process this website",
        128: "Postprocessor error (issues with file processing after download)"
    }
    
    SPECIAL_ERROR_MESSAGES = {
        64: "Unsupported URL or site - this website is not supported by gallery-dl"
    }
    
    @staticmethod
    def check_installation() -> Tuple[bool, str]:
        """Check if gallery-dl is installed and accessible."""
        # Try gallery-dl command first
        try:
            result = subprocess.run(["gallery-dl", "--version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip()
                return True, f"Gallery-dl found: {version}"
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        # Try python -m gallery_dl
        try:
            result = subprocess.run([sys.executable, "-m", "gallery_dl", "--version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip()
                return True, f"Gallery-dl found (Python module): {version}"
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        return False, "Gallery-dl not found. Please install it first: pip install gallery-dl"
    
    @staticmethod
    def test_url(url: str) -> Tuple[bool, str, List[str]]:
        """Test URL without downloading."""
        if not url.strip():
            return False, "Please enter a URL", []
        
        try:
            # Parse URL to show basic info
            parsed = urlparse(url)
            domain = parsed.netloc
            
            # Try gallery-dl command first
            cmd = ["gallery-dl", "--no-download", "--simulate", url]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            except FileNotFoundError:
                # Fallback to python -m gallery_dl
                cmd = [sys.executable, "-m", "gallery_dl", "--no-download", "--simulate", url]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            output_lines = []
            if result.stdout:
                output_lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            
            if result.returncode == 0:
                success_msg = f"✓ URL test successful for {domain} - gallery-dl can process this URL"
                return True, success_msg, output_lines
            else:
                exit_code = result.returncode
                error_desc = GalleryDLService.get_error_description(exit_code)
                
                # Analyze output for more specific context
                all_output = []
                if result.stdout:
                    all_output.extend(result.stdout.split('\n'))
                if result.stderr:
                    all_output.extend(result.stderr.split('\n'))
                
                error_context = GalleryDLService.analyze_error_output(all_output, exit_code)
                
                error_msg = f"✗ URL test failed for {domain} (exit code: {exit_code})\nReason: {error_desc}"
                if error_context:
                    error_msg += f"\nContext: {error_context}"
                
                return False, error_msg, output_lines
                
        except subprocess.TimeoutExpired:
            return False, "✗ Test timeout - URL may be slow to respond or invalid", []
        except Exception as e:
            return False, f"✗ Test error: {str(e)}", []
    
    @staticmethod
    def get_error_description(exit_code: int) -> str:
        """Get human-readable description for gallery-dl exit codes."""
        if exit_code in GalleryDLService.SPECIAL_ERROR_MESSAGES:
            return GalleryDLService.SPECIAL_ERROR_MESSAGES[exit_code]
        
        return GalleryDLService.ERROR_DESCRIPTIONS.get(
            exit_code, f"Unknown error (exit code {exit_code})"
        )
    
    @staticmethod
    def analyze_error_output(output_lines: List[str], exit_code: int) -> Optional[str]:
        """Analyze gallery-dl output to provide specific error context."""
        output_text = " ".join(output_lines).lower()
        
        # Check for common error patterns
        if "unsupported url" in output_text:
            # Extract the URL or site name for context
            for line in output_lines:
                if "Unsupported URL" in line:
                    if "shutterstock" in line.lower():
                        return "Shutterstock is not supported by gallery-dl (commercial stock photo site)"
                    elif "getty" in line.lower():
                        return "Getty Images is not supported (commercial stock photo site)"
                    elif "adobe stock" in line.lower():
                        return "Adobe Stock is not supported (commercial stock photo site)"
                    else:
                        return "This website is not supported by gallery-dl"
        
        if exit_code == 6 and ("login" in output_text or "authentication" in output_text):
            return "This site requires login credentials - try using the Authentication tab"
        
        if exit_code == 8 and ("extractor" in output_text or "format" in output_text):
            return "Website structure may have changed - try updating gallery-dl"
        
        if exit_code == 16 and ("permission" in output_text or "access" in output_text):
            return "Check file permissions and available disk space"
        
        if "network" in output_text or "connection" in output_text or "timeout" in output_text:
            return "Network connectivity issue - check your internet connection"
        
        return None
    
    @staticmethod
    def create_download_process(cmd: List[str]) -> subprocess.Popen:
        """Create a subprocess for downloading."""
        try:
            return subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1, universal_newlines=True
            )
        except FileNotFoundError:
            # Fallback to python -m gallery_dl
            cmd[0] = sys.executable
            cmd.insert(1, "-m")
            cmd.insert(2, "gallery_dl")
            return subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1, universal_newlines=True
            )
