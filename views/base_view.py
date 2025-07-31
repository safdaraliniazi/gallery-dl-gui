"""
Base view components for Gallery-DL GUI.
"""
import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod


class BaseView(ABC):
    """Base class for all view components."""
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = None
        self.create_widgets()
    
    @abstractmethod
    def create_widgets(self):
        """Create the widgets for this view."""
        pass
    
    def get_frame(self) -> ttk.Frame:
        """Get the main frame for this view."""
        return self.frame


class BaseTab(BaseView):
    """Base class for tab components."""
    
    def __init__(self, notebook: ttk.Notebook, title: str):
        self.notebook = notebook
        self.title = title
        super().__init__(notebook)
        
    def create_widgets(self):
        """Create the main frame and add to notebook."""
        self.frame = ttk.Frame(self.notebook)
        self.notebook.add(self.frame, text=self.title)
        self.setup_tab()
    
    @abstractmethod
    def setup_tab(self):
        """Setup the tab content."""
        pass
