#!/usr/bin/env python3
"""
Build script for creating standalone executables of Gallery-DL GUI.

This script uses PyInstaller to create standalone executables that include
all dependencies and can run on systems without Python installed.

Usage:
    python build_executable.py [options]

Options:
    --platform {windows,linux,macos,auto}  Target platform (default: auto)
    --console                               Include console window (for debugging)
    --name NAME                            Custom executable name
    --clean                                Clean build directories first
    --debug                                Enable debug mode
    --help                                 Show this help message

Examples:
    python build_executable.py                          # Auto-detect platform
    python build_executable.py --platform windows       # Build for Windows
    python build_executable.py --console --debug        # Debug build with console
    python build_executable.py --clean --name MyGUI     # Clean build with custom name
"""

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


class ExecutableBuilder:
    """Builds standalone executables using PyInstaller."""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.project_name = "Gallery-DL-GUI"
        self.main_script = "gallery_dl_gui.py"
        self.icon_file = "icon.ico" if os.name == 'nt' else None
        
        # Platform detection
        self.current_platform = self._detect_platform()
        
    def _detect_platform(self):
        """Detect current platform."""
        system = platform.system().lower()
        if system == "windows":
            return "windows"
        elif system == "darwin":
            return "macos"
        elif system == "linux":
            return "linux"
        else:
            return "unknown"
    
    def _check_requirements(self):
        """Check if all requirements are installed."""
        print("Checking requirements...")
        
        # Check if PyInstaller is installed
        try:
            import PyInstaller
            print(f"[OK] PyInstaller {PyInstaller.__version__} found")
        except ImportError:
            print("[INFO] PyInstaller not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("[OK] PyInstaller installed")
        
        # Check if main script exists
        if not (self.script_dir / self.main_script).exists():
            raise FileNotFoundError(f"Main script {self.main_script} not found")
        
        # Check if required modules exist
        required_dirs = ["controllers", "models", "views", "utils"]
        for dir_name in required_dirs:
            if not (self.script_dir / dir_name).exists():
                raise FileNotFoundError(f"Required directory {dir_name} not found")
        
        print("[OK] All requirements satisfied")
    
    def _get_pyinstaller_args(self, target_platform, console=False, custom_name=None, debug=False):
        """Generate PyInstaller arguments."""
        name = custom_name or f"{self.project_name}-{target_platform.title()}"
        
        args = [
            "pyinstaller",
            "--onefile",  # Create single executable file
            "--name", name,
        ]
        
        # Window mode (no console unless debugging)
        if not console:
            if target_platform == "windows":
                args.append("--windowed")
            elif target_platform in ["linux", "macos"]:
                args.append("--windowed")
        
        # Add data files and directories
        data_files = [
            ("supportedsites.md", "."),
            ("models", "models"),
            ("views", "views"), 
            ("controllers", "controllers"),
            ("utils", "utils"),
        ]
        
        for src, dst in data_files:
            if (self.script_dir / src).exists():
                if target_platform == "windows":
                    args.extend(["--add-data", f"{src};{dst}"])
                else:
                    args.extend(["--add-data", f"{src}:{dst}"])
        
        # Hidden imports (ensure these modules are included)
        hidden_imports = [
            "gallery_dl",
            "requests", 
            "PIL",
            "PIL.Image",
            "tkinter",
            "tkinter.ttk",
            "tkinter.filedialog",
            "tkinter.messagebox",
            "json",
            "threading",
            "subprocess",
            "pathlib",
            "urllib.parse",
            "webbrowser",
        ]
        
        for module in hidden_imports:
            args.extend(["--hidden-import", module])
        
        # Icon (Windows only)
        if target_platform == "windows" and self.icon_file and (self.script_dir / self.icon_file).exists():
            args.extend(["--icon", self.icon_file])
        
        # Debug options
        if debug:
            args.extend([
                "--debug", "all",
                "--log-level", "DEBUG"
            ])
        
        # Exclude modules we don't need (reduces file size)
        excludes = [
            "matplotlib",
            "scipy", 
            "numpy",
            "pandas",
            "jupyter",
            "IPython",
            "notebook",
            "pytest",
            "unittest",
        ]
        
        for module in excludes:
            args.extend(["--exclude-module", module])
        
        # Main script
        args.append(self.main_script)
        
        return args
    
    def _clean_build_dirs(self):
        """Clean build and dist directories."""
        print("Cleaning build directories...")
        
        dirs_to_clean = ["build", "dist", "__pycache__"]
        files_to_clean = ["*.spec"]
        
        for dir_name in dirs_to_clean:
            dir_path = self.script_dir / dir_name
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"[OK] Removed {dir_name}/")
        
        # Clean spec files
        for spec_file in self.script_dir.glob("*.spec"):
            spec_file.unlink()
            print(f"[OK] Removed {spec_file.name}")
    
    def build(self, target_platform=None, console=False, custom_name=None, clean=False, debug=False):
        """Build the executable."""
        if target_platform is None:
            target_platform = self.current_platform
        
        print(f"Building Gallery-DL GUI executable for {target_platform}...")
        print(f"Project directory: {self.script_dir}")
        
        # Check requirements
        self._check_requirements()
        
        # Clean if requested
        if clean:
            self._clean_build_dirs()
        
        # Change to project directory
        original_cwd = os.getcwd()
        os.chdir(self.script_dir)
        
        try:
            # Build executable
            args = self._get_pyinstaller_args(target_platform, console, custom_name, debug)
            print(f"Running: {' '.join(args)}")
            
            result = subprocess.run(args, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("[OK] Build completed successfully!")
                
                # Find the executable
                dist_dir = self.script_dir / "dist"
                if dist_dir.exists():
                    executables = list(dist_dir.glob("*"))
                    if executables:
                        exe_path = executables[0]
                        exe_size = exe_path.stat().st_size / (1024 * 1024)  # MB
                        print(f"[OK] Executable created: {exe_path}")
                        print(f"[OK] File size: {exe_size:.1f} MB")
                        
                        # Show platform-specific instructions
                        self._show_usage_instructions(exe_path, target_platform)
                    else:
                        print("[WARNING] Build completed but no executable found in dist/")
                else:
                    print("[WARNING] Build completed but dist/ directory not found")
            else:
                print("[ERROR] Build failed!")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
                return False
                
        finally:
            os.chdir(original_cwd)
        
        return True
    
    def _show_usage_instructions(self, exe_path, target_platform):
        """Show platform-specific usage instructions."""
        print("\n" + "="*60)
        print("USAGE INSTRUCTIONS")
        print("="*60)
        
        if target_platform == "windows":
            print(f"Windows: Double-click {exe_path.name}")
            print("Or run from command line:", exe_path.name)
        
        elif target_platform == "linux":
            print(f"Linux: Make executable and run:")
            print(f"  chmod +x {exe_path.name}")
            print(f"  ./{exe_path.name}")
        
        elif target_platform == "macos":
            if exe_path.suffix == ".app":
                print(f"macOS: Double-click {exe_path.name}")
            else:
                print(f"macOS: Make executable and run:")
                print(f"  chmod +x {exe_path.name}")
                print(f"  ./{exe_path.name}")
        
        print("\nFor distribution:")
        print(f"- Upload {exe_path.name} to GitHub releases")
        print("- Users can download and run without Python installation")
        print("- Include usage instructions in release notes")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Build standalone executable for Gallery-DL GUI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        "--platform",
        choices=["windows", "linux", "macos", "auto"],
        default="auto",
        help="Target platform (default: auto-detect)"
    )
    
    parser.add_argument(
        "--console",
        action="store_true",
        help="Include console window (useful for debugging)"
    )
    
    parser.add_argument(
        "--name",
        help="Custom executable name"
    )
    
    parser.add_argument(
        "--clean",
        action="store_true", 
        help="Clean build directories before building"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode with verbose output"
    )
    
    args = parser.parse_args()
    
    # Handle auto platform detection
    target_platform = args.platform
    if target_platform == "auto":
        builder = ExecutableBuilder()
        target_platform = builder.current_platform
        if target_platform == "unknown":
            print("✗ Unable to auto-detect platform. Please specify --platform")
            return 1
    
    try:
        builder = ExecutableBuilder()
        success = builder.build(
            target_platform=target_platform,
            console=args.console,
            custom_name=args.name,
            clean=args.clean,
            debug=args.debug
        )
        
        return 0 if success else 1
        
    except Exception as e:
        print(f"[ERROR] Build failed: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
