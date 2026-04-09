import feedparser
import re

FEEDS = {
    "Forbes Tech": "https://www.forbes.com/innovation/feed/",
    "Forbes AI": "https://www.forbes.com/ai/feed/",
    "MIT Tech Review": "https://www.technologyreview.com/feed/",
    "Harvard Business Review": "https://feeds.hbr.org/harvardbusiness",
}

FALLBACK_IMAGES = {
    "Forbes": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&h=340&fit=crop",
    "MIT": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&h=340&fit=crop",
    "Harvard": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=600&h=340&fit=crop",
    "LinkedIn": "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=600&h=340&fit=crop",
}

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

def get_all_articles():
    articles = []
    for source, url in FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:4]:
                pub = entry.get("published", "")
                articles.append({
                    "title": entry.get("title", "Untitled"),
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
    articles = get_all_articles()
    return articles[0] if articles else None

def get_recommended():
    articles = get_all_articles()
    return articles[1:4]

def get_three_col():
    articles = get_all_articles()
    return articles[4:7]

def get_four_col():
    articles = get_all_articles()
    return articles[7:11]

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