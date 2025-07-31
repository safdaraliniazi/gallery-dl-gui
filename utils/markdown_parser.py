"""
Markdown parser utility for Gallery-DL GUI.
"""
import re
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SiteInfo:
    """Site information parsed from supportedsites.md."""
    name: str
    url: str
    capabilities: str
    authentication: str


class MarkdownParser:
    """Parser for supportedsites.md file."""
    
    @staticmethod
    def parse_supported_sites(file_path: str) -> List[SiteInfo]:
        """Parse the supportedsites.md file and extract site information."""
        sites = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find the table section
            table_pattern = r'<tbody[^>]*>(.*?)</tbody>'
            table_match = re.search(table_pattern, content, re.DOTALL)
            
            if not table_match:
                return sites
            
            table_content = table_match.group(1)
            
            # Extract table rows
            row_pattern = r'<tr[^>]*>(.*?)</tr>'
            rows = re.findall(row_pattern, table_content, re.DOTALL)
            
            for row in rows:
                # Extract table cells
                cell_pattern = r'<td[^>]*>(.*?)</td>'
                cells = re.findall(cell_pattern, row, re.DOTALL)
                
                if len(cells) >= 4:
                    name = MarkdownParser._clean_text(cells[0])
                    url_html = cells[1]
                    capabilities = MarkdownParser._clean_text(cells[2])
                    authentication = MarkdownParser._clean_text(cells[3])
                    
                    # Extract URL from HTML
                    url = MarkdownParser._extract_url(url_html)
                    
                    if name and url:
                        sites.append(SiteInfo(
                            name=name,
                            url=url,
                            capabilities=capabilities,
                            authentication=authentication
                        ))
        
        except Exception as e:
            print(f"Error parsing supportedsites.md: {e}")
        
        return sites
    
    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean HTML tags and extra whitespace from text."""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Clean up whitespace
        text = ' '.join(text.split())
        return text.strip()
    
    @staticmethod
    def _extract_url(url_html: str) -> str:
        """Extract URL from HTML anchor tag."""
        # Look for href attribute
        href_match = re.search(r'href=["\']([^"\']+)["\']', url_html)
        if href_match:
            return href_match.group(1)
        
        # If no href found, try to extract plain URL
        url_match = re.search(r'https?://[^\s<>"]+', url_html)
        if url_match:
            return url_match.group(0)
        
        return ""
    
    @staticmethod
    def categorize_site(site_name: str, capabilities: str) -> str:
        """Categorize a site based on its name and capabilities."""
        name_lower = site_name.lower()
        caps_lower = capabilities.lower()
        
        # Image boards and galleries
        if any(term in name_lower for term in ['booru', 'chan', 'gel', 'rule34']):
            return "Image Boards"
        
        # Art platforms
        if any(term in name_lower for term in ['art', 'deviant', 'pixiv', 'behance']):
            return "Art Platforms"
        
        # Social media
        if any(term in name_lower for term in ['twitter', 'instagram', 'tumblr', 'facebook', 'reddit']):
            return "Social Media"
        
        # Manga/Comics
        if any(term in caps_lower for term in ['manga', 'comic', 'chapter']):
            return "Manga/Comics"
        
        # Photography
        if any(term in name_lower for term in ['photo', 'flickr', '500px']):
            return "Photography"
        
        # Forums
        if any(term in caps_lower for term in ['board', 'thread', 'forum']):
            return "Forums"
        
        # Video platforms
        if any(term in caps_lower for term in ['video', 'youtube', 'vimeo']):
            return "Video Platforms"
        
        return "Other"
