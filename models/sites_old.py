"""
Supported sites data model for Gallery-DL GUI.
"""
from typing import List, Tuple, NamedTuple
from dataclasses import dataclass


@dataclass
class SiteInfo:
    """Information about a supported site."""
    name: str
    category: str
    description: str


class SitesDatabase:
    """Database of supported sites."""
    
    @staticmethod
    def get_all_sites() -> List[SiteInfo]:
        """Get comprehensive list of all supported sites."""
        sites_data = [
            # Social Media & Communication
            ("Twitter", "Social Media", "Tweets, images, videos from Twitter/X"),
            ("Instagram", "Social Media", "Posts, stories, reels from Instagram"),
            ("Facebook", "Social Media", "Posts and media from Facebook"),
            ("TikTok", "Social Media", "Videos from TikTok"),
            ("Reddit", "Social Media", "Posts and media from Reddit"),
            ("Tumblr", "Social Media", "Posts from Tumblr blogs"),
            ("LinkedIn", "Social Media", "Professional posts and media"),
            ("Pinterest", "Social Media", "Pins and boards from Pinterest"),
            ("Flickr", "Social Media", "Photos from Flickr"),
            ("Discord", "Social Media", "Media from Discord channels"),
            ("Telegram", "Social Media", "Media from Telegram channels"),
            ("WeChat", "Social Media", "WeChat posts and media"),
            ("VKontakte", "Social Media", "Posts from VK.com"),
            ("Mastodon", "Social Media", "Posts from Mastodon instances"),
            
            # Art & Design Platforms
            ("DeviantArt", "Art & Design", "Artworks from DeviantArt"),
            ("Pixiv", "Art & Design", "Japanese art community platform"),
            ("ArtStation", "Art & Design", "Professional art portfolios"),
            ("Behance", "Art & Design", "Creative portfolios from Adobe Behance"),
            ("Dribbble", "Art & Design", "Design shots and portfolios"),
            ("Newgrounds", "Art & Design", "Art, games, and animations"),
            ("FurAffinity", "Art & Design", "Furry art community"),
            ("Weasyl", "Art & Design", "Art sharing platform"),
            ("Inkbunny", "Art & Design", "Art community platform"),
            ("SoFurry", "Art & Design", "Furry art and stories"),
            ("e621", "Art & Design", "Furry art database"),
            ("e926", "Art & Design", "Safe furry art database"),
            ("Rule34", "Art & Design", "Adult art database"),
            ("Gelbooru", "Art & Design", "Anime/manga image board"),
            ("Danbooru", "Art & Design", "Anime/manga image board"),
            ("Safebooru", "Art & Design", "Safe anime/manga images"),
            ("Konachan", "Art & Design", "High-quality anime wallpapers"),
            ("Yande.re", "Art & Design", "Anime image board"),
            ("Sankaku Complex", "Art & Design", "Anime and idol images"),
            
            # Image Boards & Forums
            ("4chan", "Image Boards", "Anonymous image board"),
            ("8kun", "Image Boards", "Image board platform"),
            ("Lainchan", "Image Boards", "Technology-focused image board"),
            ("4plebs", "Image Boards", "4chan archive"),
            ("Desu Archive", "Image Boards", "4chan archive"),
            ("Archived.moe", "Image Boards", "4chan archive"),
            
            # Manga & Comics
            ("MangaDex", "Manga & Comics", "Multilingual manga platform"),
            ("Mangakakalot", "Manga & Comics", "Manga reading site"),
            ("Mangapark", "Manga & Comics", "Manga aggregator"),
            ("Batoto", "Manga & Comics", "Manga community"),
            ("Dynasty Reader", "Manga & Comics", "Yuri manga scanlations"),
            ("Webtoons", "Manga & Comics", "Digital comics platform"),
            ("Tapas", "Manga & Comics", "Web comics and novels"),
            ("Comic Walker", "Manga & Comics", "Japanese digital manga"),
            ("Comico", "Manga & Comics", "Japanese webtoon platform"),
            ("MangaPlus", "Manga & Comics", "Official Shueisha manga"),
            ("Viz Media", "Manga & Comics", "Official English manga"),
            
            # Video Platforms
            ("YouTube", "Video", "Videos from YouTube"),
            ("Vimeo", "Video", "Videos from Vimeo"),
            ("Twitch", "Video", "Clips and videos from Twitch"),
            ("Bilibili", "Video", "Chinese video platform"),
            ("Niconico", "Video", "Japanese video platform"),
            ("PornHub", "Video", "Adult video platform"),
            ("XNXX", "Video", "Adult video platform"),
            ("XVideos", "Video", "Adult video platform"),
            ("YouPorn", "Video", "Adult video platform"),
            ("Redtube", "Video", "Adult video platform"),
            
            # Photography
            ("500px", "Photography", "Professional photography"),
            ("SmugMug", "Photography", "Photography hosting"),
            ("Photobucket", "Photography", "Photo sharing service"),
            ("ImageFap", "Photography", "Adult photo sharing"),
            ("ImageVenue", "Photography", "Image hosting service"),
            ("PostImage", "Photography", "Image hosting service"),
            ("ImgBB", "Photography", "Image hosting service"),
            
            # Adult Content
            ("OnlyFans", "Adult", "Subscription adult content"),
            ("Patreon", "Adult", "Creator subscriptions (adult content)"),
            ("Fansly", "Adult", "Adult content subscriptions"),
            ("JustFor.Fans", "Adult", "Adult content platform"),
            ("ManyVids", "Adult", "Adult video marketplace"),
            ("Chaturbate", "Adult", "Adult webcam platform"),
            ("Kemono", "Adult", "Patreon content archive"),
            ("Coomer", "Adult", "OnlyFans content archive"),
            ("Exhentai", "Adult", "Adult doujin gallery"),
            ("Nhentai", "Adult", "Doujin manga platform"),
            ("Hitomi", "Adult", "Adult manga and CG"),
            ("Tsumino", "Adult", "Adult doujin platform"),
            ("Simply Hentai", "Adult", "Adult manga platform"),
            
            # Professional & Business
            ("LinkedIn", "Professional", "Professional networking"),
            ("SlideShare", "Professional", "Presentation sharing"),
            ("Academia.edu", "Professional", "Academic papers and research"),
            ("ResearchGate", "Professional", "Scientific publications"),
            ("Issuu", "Professional", "Digital publishing"),
            
            # Gaming
            ("Steam", "Gaming", "Game screenshots and artwork"),
            ("itch.io", "Gaming", "Indie game platform"),
            ("Game Jolt", "Gaming", "Indie game community"),
            ("Gamersyde", "Gaming", "Gaming media"),
            ("NexusMods", "Gaming", "Game modification files"),
            
            # File Hosting
            ("Imgur", "File Hosting", "Image hosting service"),
            ("ImageBam", "File Hosting", "Image hosting service"),
            ("ImageTwist", "File Hosting", "Image hosting service"),
            ("PixHost", "File Hosting", "Image hosting service"),
            ("TurboImageHost", "File Hosting", "Image hosting service"),
            ("ImageShack", "File Hosting", "Image hosting service"),
            ("TinyPic", "File Hosting", "Image hosting service"),
            ("MediaFire", "File Hosting", "File hosting service"),
            ("Mega", "File Hosting", "Cloud storage service"),
            ("Dropbox", "File Hosting", "Cloud storage service"),
            ("Google Drive", "File Hosting", "Cloud storage service"),
            ("OneDrive", "File Hosting", "Microsoft cloud storage"),
            
            # News & Media
            ("BBC", "News & Media", "BBC news articles and media"),
            ("CNN", "News & Media", "CNN news content"),
            ("Reuters", "News & Media", "Reuters news media"),
            ("Associated Press", "News & Media", "AP news content"),
            ("The Guardian", "News & Media", "Guardian news media"),
            ("New York Times", "News & Media", "NYT articles and media"),
            ("Washington Post", "News & Media", "WaPo content"),
            
            # Regional Platforms
            ("Weibo", "Regional", "Chinese microblogging platform"),
            ("QQ", "Regional", "Chinese social platform"),
            ("Baidu", "Regional", "Chinese search and services"),
            ("Naver", "Regional", "Korean web services"),
            ("Line", "Regional", "Japanese messaging app"),
            ("Kakao", "Regional", "Korean platform"),
            ("Yandex", "Regional", "Russian web services"),
            ("Mail.ru", "Regional", "Russian web platform"),
            ("Odnoklassniki", "Regional", "Russian social network"),
            
            # Specialized
            ("Wikipedia", "Reference", "Encyclopedia articles and media"),
            ("Wikimedia Commons", "Reference", "Free media repository"),
            ("Archive.org", "Reference", "Internet archive"),
            ("Unsplash", "Stock", "Free stock photography"),
            ("Pexels", "Stock", "Free stock photos"),
            
            # Adult Specialized
            ("JoyReactor", "Adult", "Russian image board"),
            ("Lolibooru", "Adult", "Specialized image board"),
            ("ATFBooru", "Adult", "Adult image board"),
            ("Realbooru", "Adult", "Adult image board"),
            ("3DBooru", "Adult", "3D adult art"),
            ("PornPics", "Adult", "Adult photo galleries"),
            ("Sex.com", "Adult", "Adult content aggregator"),
            ("Erome", "Adult", "Adult media platform"),
            ("ImageFap", "Adult", "Adult photo sharing"),
            
            # Miscellaneous
            ("SoundCloud", "Audio", "Audio tracks and podcasts"),
            ("Bandcamp", "Audio", "Independent music platform"),
            ("Spotify", "Audio", "Music streaming (limited)"),
            ("Last.fm", "Audio", "Music tracking and discovery"),
            ("Grooveshark", "Audio", "Music streaming (archived)"),
            ("8tracks", "Audio", "Playlist sharing"),
            ("Mixcloud", "Audio", "DJ mixes and radio shows"),
            
            # Tech & Development
            ("GitHub", "Development", "Code repositories and media"),
            ("GitLab", "Development", "Code hosting platform"),
            ("Bitbucket", "Development", "Code repository hosting"),
            ("SourceForge", "Development", "Open source project hosting"),
            ("CodePen", "Development", "Front-end code sharing"),
            ("JSFiddle", "Development", "Code snippet sharing"),
            
            # Educational
            ("Khan Academy", "Educational", "Educational videos"),
            ("Coursera", "Educational", "Online course content"),
            ("edX", "Educational", "Educational platform"),
            ("Udemy", "Educational", "Online learning platform"),
            ("TED", "Educational", "TED talk videos"),
            ("YouTube EDU", "Educational", "Educational YouTube content"),
            
            # Shopping & E-commerce
            ("Amazon", "E-commerce", "Product images and media"),
            ("eBay", "E-commerce", "Auction and product images"),
            ("Etsy", "E-commerce", "Handmade product images"),
            ("AliExpress", "E-commerce", "Product images"),
            ("Wish", "E-commerce", "Product media"),
            ("Shopify", "E-commerce", "Store product images"),
            
            # Dating & Social
            ("Tinder", "Dating", "Profile images (limited)"),
            ("Bumble", "Dating", "Dating app content"),
            ("OKCupid", "Dating", "Dating profile media"),
            ("Match.com", "Dating", "Dating platform content"),
            
            # Streaming & Live
            ("Periscope", "Live Streaming", "Live stream archives"),
            ("YouNow", "Live Streaming", "Live streaming platform"),
            ("Bigo Live", "Live Streaming", "Live video streaming"),
            ("LiveMe", "Live Streaming", "Live streaming app"),
            
            # Cryptocurrency & NFT
            ("OpenSea", "NFT", "NFT marketplace"),
            ("SuperRare", "NFT", "Digital art NFTs"),
            ("Foundation", "NFT", "NFT art platform"),
            ("Async Art", "NFT", "Programmable art NFTs"),
            
            # Travel & Lifestyle
            ("Airbnb", "Travel", "Property images"),
            ("TripAdvisor", "Travel", "Travel photos and reviews"),
            ("Booking.com", "Travel", "Hotel and travel images"),
            ("Expedia", "Travel", "Travel content"),
            
            # Food & Cooking
            ("Allrecipes", "Food", "Recipe images"),
            ("Food Network", "Food", "Cooking show content"),
            ("Tasty", "Food", "Recipe videos and images"),
            ("Epicurious", "Food", "Food and recipe media"),
            
            # Fashion & Beauty
            ("Vogue", "Fashion", "Fashion photography"),
            ("Elle", "Fashion", "Fashion magazine content"),
            ("Harper's Bazaar", "Fashion", "Fashion media"),
            ("Sephora", "Beauty", "Beauty product images"),
            
            # Sports
            ("ESPN", "Sports", "Sports news and media"),
            ("Sports Illustrated", "Sports", "Sports photography"),
            ("Olympic.org", "Sports", "Olympic content"),
            ("FIFA", "Sports", "Football/soccer content"),
            
            # Music & Entertainment
            ("Billboard", "Music", "Music industry content"),
            ("Rolling Stone", "Music", "Music journalism"),
            ("Pitchfork", "Music", "Music reviews and media"),
            ("MTV", "Entertainment", "Music and entertainment"),
            
            # Science & Technology
            ("NASA", "Science", "Space imagery and videos"),
            ("National Geographic", "Science", "Nature and science media"),
            ("Scientific American", "Science", "Science journalism"),
            ("Popular Science", "Science", "Science and technology"),
            
            # More specialized platforms
            ("Booth", "Japanese", "Japanese digital marketplace"),
            ("Pixiv Fanbox", "Japanese", "Japanese creator platform"),
            ("Fantia", "Japanese", "Japanese fan platform"),
            ("Dlsite", "Japanese", "Japanese digital content"),
            ("DMM", "Japanese", "Japanese digital marketplace"),
            ("Nico Seiga", "Japanese", "Japanese illustration platform"),
            ("Tinami", "Japanese", "Japanese art community"),
            ("BCY", "Chinese", "Chinese illustration platform"),
            ("Lofter", "Chinese", "Chinese blogging platform"),
            ("Huaban", "Chinese", "Chinese Pinterest-like platform"),
        ]
        
        # Convert to SiteInfo objects and sort by name
        sites = [SiteInfo(name, category, description) for name, category, description in sites_data]
        sites.sort(key=lambda x: x.name.lower())
        
        return sites
    
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
