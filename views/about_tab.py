"""
About tab view for Gallery-DL GUI.
"""
import tkinter as tk
from tkinter import ttk
from views.base_view import BaseTab
from models.settings import AppState
from models.sites import SitesDatabase
from utils.cef_web_preview import CEFWebPreview, cef_message_loop_work, CEF_AVAILABLE


class AboutTab(BaseTab):
    """About tab with application info and supported sites list with CEF web preview."""
    
    def __init__(self, notebook: ttk.Notebook, app_state: AppState):
        self.app_state = app_state
        self.all_sites = []
        self.filtered_sites = []
        self.web_preview = None
        self.cef_message_loop_active = False
        super().__init__(notebook, "About")
    
    def setup_tab(self):
        """Setup the about tab content with improved layout."""
        # Create main container with paned window for resizable sections
        self.main_paned = ttk.PanedWindow(self.frame, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Left side - Info and sites list (40% of width)
        self.left_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.left_frame, weight=2)
        
        # Right side - Web preview (60% of width)
        self.right_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.right_frame, weight=3)
        
        # Setup left side content with vertical layout
        self._create_left_content()
        
        # Setup right side content
        self._create_right_content()
        
        # Load sites data
        self._populate_sites()
        
        # Start CEF message loop if available
        if CEF_AVAILABLE:
            self._start_cef_message_loop()
    
    def _create_left_content(self):
        """Create left side content with better space utilization."""
        # Create vertical paned window for left side
        self.left_paned = ttk.PanedWindow(self.left_frame, orient=tk.VERTICAL)
        self.left_paned.pack(fill="both", expand=True)
        
        # Top section - Application info (30% of height)
        self.info_frame = ttk.Frame(self.left_paned)
        self.left_paned.add(self.info_frame, weight=1)
        
        # Bottom section - Sites list (70% of height)
        self.sites_frame = ttk.Frame(self.left_paned)
        self.left_paned.add(self.sites_frame, weight=3)
        
        # Create sections
        self._create_info_section(self.info_frame)
        self._create_sites_section(self.sites_frame)
    
    def _create_right_content(self):
        """Create right side content (CEF web preview)."""
        self.web_preview = CEFWebPreview(self.right_frame, width=800, height=600)
        self.web_preview.pack(fill="both", expand=True)
    
    def _create_info_section(self, parent):
        """Create compact application info section."""
        info_frame = ttk.LabelFrame(parent, text="Gallery-DL GUI", padding="8")
        info_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Compact about text
        about_text = """A modern GUI for gallery-dl - download from 300+ websites!

✨ Features: Real-time progress, authentication, URL testing
🌐 Sites: Twitter, Instagram, DeviantArt, Pixiv, and many more
🔗 Project: https://github.com/mikf/gallery-dl"""
        
        info_label = ttk.Label(info_frame, text=about_text, justify=tk.LEFT, 
                              font=("Arial", 9), wraplength=350)
        info_label.pack(fill="both", expand=True)
    
    def _create_sites_section(self, parent):
        """Create sites section with better layout."""
        sites_container = ttk.LabelFrame(parent, text="Supported Websites", padding="5")
        sites_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Search controls at top
        self._create_search_controls(sites_container)
        
        # Sites tree below search
        self._create_sites_tree(sites_container)
    
    def _create_search_controls(self, parent):
        """Create compact search functionality."""
        search_frame = ttk.Frame(parent)
        search_frame.pack(fill="x", pady=(0, 8))
        
        # Search row
        search_row = ttk.Frame(search_frame)
        search_row.pack(fill="x", pady=(0, 5))
        
        ttk.Label(search_row, text="Search:", font=("Arial", 9)).pack(side="left")
        self.app_state.search_var.trace("w", self._filter_sites)
        search_entry = ttk.Entry(search_row, textvariable=self.app_state.search_var, 
                                font=("Arial", 9))
        search_entry.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        # Category row
        category_row = ttk.Frame(search_frame)
        category_row.pack(fill="x")
        
        ttk.Label(category_row, text="Category:", font=("Arial", 9)).pack(side="left")
        self.app_state.category_var.trace("w", self._filter_sites)
        self.category_combo = ttk.Combobox(category_row, textvariable=self.app_state.category_var, 
                                          font=("Arial", 9), state="readonly")
        self.category_combo.pack(side="left", fill="x", expand=True, padx=(5, 0))
    
    def _create_sites_tree(self, parent):
        """Create sites tree view with better sizing."""
        sites_list_frame = ttk.Frame(parent)
        sites_list_frame.pack(fill="both", expand=True)
        
        # Create Treeview
        columns = ("Site", "Category")
        self.sites_tree = ttk.Treeview(sites_list_frame, columns=columns, show="headings")
        
        # Configure columns - simplified for space
        self.sites_tree.heading("Site", text="Website")
        self.sites_tree.heading("Category", text="Category")
        
        self.sites_tree.column("Site", width=200, anchor="w")
        self.sites_tree.column("Category", width=120, anchor="center")
        
        # Add scrollbar
        tree_scrollbar = ttk.Scrollbar(sites_list_frame, orient="vertical", 
                                      command=self.sites_tree.yview)
        self.sites_tree.configure(yscrollcommand=tree_scrollbar.set)
        
        # Bind events
        self.sites_tree.bind("<<TreeviewSelect>>", self._on_site_select)
        self.sites_tree.bind("<Double-1>", self._on_site_double_click)
        
        # Pack with proper grid
        self.sites_tree.grid(row=0, column=0, sticky="nsew")
        tree_scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure grid weights
        sites_list_frame.grid_rowconfigure(0, weight=1)
        sites_list_frame.grid_columnconfigure(0, weight=1)
    
    def _on_site_select(self, event):
        """Handle site selection for web preview."""
        selection = self.sites_tree.selection()
        if selection and self.web_preview:
            item = selection[0]
            values = self.sites_tree.item(item, "values")
            if values:
                site_name = values[0]
                # Find the site info to get the URL
                for site in self.filtered_sites:
                    if site.name == site_name:
                        if site.url:
                            self.web_preview.load_url(site.url, site.name)
                        break
    
    def _on_site_double_click(self, event):
        """Handle double-click to open site in browser."""
        selection = self.sites_tree.selection()
        if selection:
            item = selection[0]
            values = self.sites_tree.item(item, "values")
            if values:
                site_name = values[0]
                # Find the site info to get the URL
                for site in self.filtered_sites:
                    if site.name == site_name and site.url:
                        import webbrowser
                        webbrowser.open(site.url)
                        break
    
    def _populate_sites(self):
        """Populate the sites list with data."""
        self.all_sites = SitesDatabase.get_all_sites()
        self.filtered_sites = self.all_sites.copy()
        
        # Update category combobox
        categories = SitesDatabase.get_categories()
        self.category_combo['values'] = categories
        
        self._update_sites_display()
    
    def _filter_sites(self, *args):
        """Filter sites based on search and category."""
        search_term = self.app_state.search_var.get()
        category = self.app_state.category_var.get()
        
        self.filtered_sites = SitesDatabase.filter_sites(self.all_sites, search_term, category)
        self._update_sites_display()
    
    def _update_sites_display(self):
        """Update the sites tree display with simplified layout."""
        # Clear existing items
        for item in self.sites_tree.get_children():
            self.sites_tree.delete(item)
        
        # Add filtered sites - simplified columns
        for site in self.filtered_sites:
            self.sites_tree.insert("", "end", values=(site.name, site.category))
        
        # Update count in sites frame title
        try:
            count = len(self.filtered_sites)
            total = len(self.all_sites)
            
            # Find and update the sites container title
            for widget in self.sites_frame.winfo_children():
                if isinstance(widget, ttk.LabelFrame):
                    if "Supported Websites" in str(widget.cget("text")):
                        widget.configure(text=f"Supported Websites ({count} of {total})")
                        break
        except:
            pass  # Ignore if frame not found
    
    def _start_cef_message_loop(self):
        """Start the CEF message loop for browser responsiveness."""
        if CEF_AVAILABLE and not self.cef_message_loop_active:
            self.cef_message_loop_active = True
            self._run_cef_message_loop()
    
    def _run_cef_message_loop(self):
        """Run CEF message loop work and schedule next iteration."""
        if self.cef_message_loop_active and CEF_AVAILABLE:
            try:
                cef_message_loop_work()
                # Schedule next iteration
                self.frame.after(10, self._run_cef_message_loop)
            except Exception as e:
                print(f"CEF message loop error: {e}")
                self.cef_message_loop_active = False
    
    def cleanup(self):
        """Cleanup CEF resources when tab is destroyed."""
        self.cef_message_loop_active = False
        if self.web_preview:
            self.web_preview.cleanup()
