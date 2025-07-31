"""
Sites database for Gallery-DL GUI.
"""
import os
from dataclasses import dataclass
from typing import List
from utils.markdown_parser import MarkdownParser, SiteInfo as ParsedSiteInfo


@dataclass
class SiteInfo:
    """Information about a supported site."""
    name: str
    category: str
    description: str
    url: str = ""
    capabilities: str = ""
    authentication: str = ""


class SitesDatabase:
    """Database of supported sites and their information."""
    
    _cached_sites: List[SiteInfo] = None
    
    @staticmethod
    def get_all_sites() -> List[SiteInfo]:
        """Get all supported sites from supportedsites.md."""
        if SitesDatabase._cached_sites is None:
            SitesDatabase._load_sites_from_markdown()
        
        return SitesDatabase._cached_sites or []
    
    @staticmethod
    def _load_sites_from_markdown() -> None:
        """Load sites from supportedsites.md file."""
        try:
            # Get the project root directory
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            markdown_file = os.path.join(current_dir, "supportedsites.md")
            
            if os.path.exists(markdown_file):
                parsed_sites = MarkdownParser.parse_supported_sites(markdown_file)
                
                SitesDatabase._cached_sites = []
                for parsed_site in parsed_sites:
                    category = MarkdownParser.categorize_site(parsed_site.name, parsed_site.capabilities)
                    
                    site_info = SiteInfo(
                        name=parsed_site.name,
                        category=category,
                        description=parsed_site.capabilities,
                        url=parsed_site.url,
                        capabilities=parsed_site.capabilities,
                        authentication=parsed_site.authentication
                    )
                    SitesDatabase._cached_sites.append(site_info)
            else:
                # Fallback to hardcoded sites if markdown file not found
                SitesDatabase._cached_sites = SitesDatabase._get_fallback_sites()
                
        except Exception as e:
            print(f"Error loading sites from markdown: {e}")
            SitesDatabase._cached_sites = SitesDatabase._get_fallback_sites()
    
    @staticmethod
    def _get_fallback_sites() -> List[SiteInfo]:
        """Get fallback sites list if markdown parsing fails."""
        return [
            # Art Platforms
            SiteInfo("DeviantArt", "Art Platforms", "Digital art galleries and collections", 
                    "https://www.deviantart.com/"),
            SiteInfo("ArtStation", "Art Platforms", "Professional art portfolios",
                    "https://www.artstation.com/"),
            SiteInfo("Pixiv", "Art Platforms", "Japanese digital art and illustrations",
                    "https://www.pixiv.net/"),
            SiteInfo("Behance", "Art Platforms", "Creative work portfolios",
                    "https://www.behance.net/"),
            
            # Social Media
            SiteInfo("Twitter", "Social Media", "Twitter posts and media",
                    "https://twitter.com/"),
            SiteInfo("Instagram", "Social Media", "Instagram posts and stories",
                    "https://www.instagram.com/"),
            SiteInfo("Tumblr", "Social Media", "Tumblr blogs and posts",
                    "https://www.tumblr.com/"),
            SiteInfo("Reddit", "Social Media", "Reddit posts and subreddits",
                    "https://www.reddit.com/"),
            
            # Image Boards
            SiteInfo("Danbooru", "Image Boards", "Anime-style artwork database",
                    "https://danbooru.donmai.us/"),
            SiteInfo("Gelbooru", "Image Boards", "Anime and manga image board",
                    "https://gelbooru.com/"),
            SiteInfo("e621", "Image Boards", "Anthropomorphic art archive",
                    "https://e621.net/"),
            
            # Photography
            SiteInfo("Flickr", "Photography", "Photo sharing and hosting",
                    "https://www.flickr.com/"),
            SiteInfo("500px", "Photography", "Photography community",
                    "https://500px.com/"),
            
            # Manga/Comics
            SiteInfo("MangaDex", "Manga/Comics", "Manga reading platform",
                    "https://mangadex.org/"),
            
            # Video Platforms
            SiteInfo("YouTube", "Video Platforms", "Video sharing platform",
                    "https://www.youtube.com/"),
            
            # Forums
            SiteInfo("4chan", "Forums", "Anonymous imageboard",
                    "https://www.4chan.org/"),
        ]
    
    @staticmethod
    def get_categories() -> List[str]:
        """Get all unique categories."""
        sites = SitesDatabase.get_all_sites()
        categories = ["All"] + sorted(set(site.category for site in sites))
        return categories
    
    @staticmethod
    def filter_sites(sites: List[SiteInfo], search_term: str = "", category: str = "All") -> List[SiteInfo]:
        """Filter sites based on search term and category."""
        filtered = []
        search_lower = search_term.lower()
        
        for site in sites:
            # Category filter
            if category != "All" and site.category != category:
                continue
            
            # Search filter
            if search_term and search_lower not in site.name.lower() and search_lower not in site.description.lower():
                continue
                
            filtered.append(site)
        
        return filtered
