import feedparser
import re

FEEDS = {
    "Forbes": "https://www.forbes.com/innovation/feed/",
    "MIT Tech Review": "https://www.technologyreview.com/feed/",
    "Harvard Business Review": "https://feeds.hbr.org/harvardbusiness",
    "McKinsey": "https://www.mckinsey.com/feeds/rss/all",
}

FALLBACK_IMAGES = {
    "Forbes": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&h=340&fit=crop",
    "McKinsey": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=600&h=340&fit=crop",
    "MIT": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&h=340&fit=crop",
    "Harvard": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=600&h=340&fit=crop",
    "LinkedIn": "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=600&h=340&fit=crop",
}

BLOCKLIST = [
    # Entertainment
    "WWE", "NFL", "NBA", "MLB", "UFC",
    "Wordle", "crossword", "puzzle",
    "celebrity", "Celebrity",
    "movie", "Movie", "Netflix", "Disney",
    "TV show", "sitcom", "comedian",
    "Invincible", "Marvel", "DC Comics",
    "music", "album", "singer", "rapper",
    "Grammy", "Oscar", "Emmy",
    # Nature/off-topic
    "shark", "Shark", "whale", "dolphin",
    "AstroTurf", "fake grass", "Tarkov","Trader","NYT","Northern Lights","Aurora",
    "Desalination", "Download:","Suleyman",
    # Sports
    "Super Bowl", "World Series", "March Madness",
    "quarterback", "touchdown", "home run",
]

PINNED_ARTICLES = [
    {
        "title": "Mustafa Suleyman: AI development won't hit a wall anytime soon—here's why",
        "summary": "The Microsoft AI CEO argues that the pace of AI progress will continue accelerating, driven by new architectures and massive investment in compute...",
        "link": "https://www.technologyreview.com/2024/02/28/1089444/mustafa-suleyman-microsoft-ai-development/",
        "source": "MIT Tech Review",
        "date": "Apr 9, 2026",
        "image": "https://images.unsplash.com/photo-1677442135703-1787eea5ce01?w=600&h=340&fit=crop",
        "tag": "MIT",
        "type": "Article",
    },
]

def extract_image(entry, source=""):
    if hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
        url = entry.media_thumbnail[0].get("url", "")
        if url:
            return url
    if hasattr(entry, "media_content") and entry.media_content:
        for m in entry.media_content:
            if m.get("url", ""):
                return m.get("url", "")
    for enc in getattr(entry, "enclosures", []):
        if enc.get("type", "").startswith("image"):
            return enc.get("href", "")
    for link in getattr(entry, "links", []):
        if link.get("type", "").startswith("image"):
            return link.get("href", "")
    content = ""
    if hasattr(entry, "content") and entry.content:
        content = entry.content[0].get("value", "")
    if not content:
        content = entry.get("summary", "") or ""
    match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', content)
    if match:
        return match.group(1)
    for key in FALLBACK_IMAGES:
        if key.lower() in source.lower():
            return FALLBACK_IMAGES[key]
    return "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&h=340&fit=crop"

def is_blocked(title):
    return any(word.lower() in title.lower() for word in BLOCKLIST)

def get_all_articles():
    articles = list(PINNED_ARTICLES)
    for source, url in FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:6]:
                title = entry.get("title", "Untitled")
                if is_blocked(title):
                    continue
                pub = entry.get("published", "")
                articles.append({
                    "title": title,
                    "summary": entry.get("summary", "")[:180] + "...",
                    "link": entry.get("link", "#"),
                    "source": source,
                    "date": pub[:16] if pub else "",
                    "image": extract_image(entry, source),
                    "tag": source.replace(" Tech", "").replace(" AI", ""),
                    "type": "Article",
                })
        except Exception as e:
            print(f"Feed error for {source}: {e}")
    return articles

def get_hero_article():
    return get_all_articles()[0]

def get_recommended():
    return get_all_articles()[1:4]

def get_three_col():
    return get_all_articles()[4:7]

def get_four_col():
    return get_all_articles()[7:11]

def get_articles():
    return get_all_articles()[:9]

def get_linkedin_posts():
    return [
        {
            "title": "Why AI Governance is the #1 Priority for Federal Contractors in 2026",
            "summary": "Organizations that build trust through transparent AI frameworks are winning more contracts.",
            "link": "https://www.linkedin.com/feed/",
            "source": "LinkedIn",
            "date": "Apr 7, 2026",
            "image": "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=600&h=340&fit=crop",
            "tag": "LinkedIn",
            "type": "Post",
        },
        {
            "title": "The 5 AI Skills Federal Agencies Are Hiring For Right Now",
            "summary": "From prompt engineering to ATO acceleration, agencies are moving fast into Q2 2026.",
            "link": "https://www.linkedin.com/feed/",
            "source": "LinkedIn",
            "date": "Apr 6, 2026",
            "image": "https://images.unsplash.com/photo-1521737711867-e3b97375f902?w=600&h=340&fit=crop",
            "tag": "LinkedIn",
            "type": "Post",
        },
        {
            "title": "Mission Value Orchestration: From Authorization to Actualization",
            "summary": "The firms closing the gap between ATO approval and real operational value.",
            "link": "https://www.linkedin.com/feed/",
            "source": "LinkedIn",
            "date": "Apr 5, 2026",
            "image": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=600&h=340&fit=crop",
            "tag": "LinkedIn",
            "type": "Post",
        },
        {
            "title": "Digital Transformation Roadmap for GovCon in 2026",
            "summary": "A structured approach to modernizing federal IT infrastructure while maintaining compliance.",
            "link": "https://www.linkedin.com/feed/",
            "source": "LinkedIn",
            "date": "Apr 4, 2026",
            "image": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=600&h=340&fit=crop",
            "tag": "LinkedIn",
            "type": "Post",
        },
    ]