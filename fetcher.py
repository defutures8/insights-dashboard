import feedparser
import re

FEEDS = {
    "Forbes Tech": "https://www.forbes.com/innovation/feed/",
    "Forbes AI": "https://www.forbes.com/ai/feed/",
    "MIT Tech Review": "https://www.technologyreview.com/feed/",
    "Harvard Business Review": "https://feeds.hbr.org/harvardbusiness",
}

def extract_image(entry):
    if hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
        return entry.media_thumbnail[0].get("url", "")
    if hasattr(entry, "media_content") and entry.media_content:
        return entry.media_content[0].get("url", "")
    for link in getattr(entry, "links", []):
        if link.get("type", "").startswith("image"):
            return link.get("href", "")
    summary = entry.get("summary", "") or ""
    match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', summary)
    if match:
        return match.group(1)
    return ""

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
                    "image": extract_image(entry),
                    "tag": source.replace(" Tech", "").replace(" AI", ""),
                    "type": "Article",
                })
        except Exception as e:
            print(f"Feed error for {source}: {e}")
    return articles

def get_articles():
    return get_all_articles()[:9]

def get_hero_article():
    articles = get_all_articles()
    return articles[0] if articles else None

def get_recommended():
    articles = get_all_articles()
    return articles[1:6]

def get_three_col():
    articles = get_all_articles()
    return articles[6:9]

def get_four_col():
    articles = get_all_articles()
    return articles[9:13]

def get_linkedin_posts():
    return [
        {
            "title": "Why AI Governance is the #1 Priority for Federal Contractors in 2026",
            "summary": "Organizations that build trust through transparent AI frameworks are winning more contracts.",
            "link": "https://www.linkedin.com/feed/",
            "source": "LinkedIn",
            "date": "Apr 7, 2026",
            "image": "https://placehold.co/600x340/0a66c2/ffffff?text=AI+Governance",
            "tag": "LinkedIn",
            "type": "Post",
        },
        {
            "title": "The 5 AI Skills Federal Agencies Are Hiring For Right Now",
            "summary": "From prompt engineering to ATO acceleration, agencies are moving fast into Q2 2026.",
            "link": "https://www.linkedin.com/feed/",
            "source": "LinkedIn",
            "date": "Apr 6, 2026",
            "image": "https://placehold.co/600x340/0a66c2/ffffff?text=Federal+AI",
            "tag": "LinkedIn",
            "type": "Post",
        },
        {
            "title": "Mission Value Orchestration: From Authorization to Actualization",
            "summary": "The firms closing the gap between ATO approval and real operational value.",
            "link": "https://www.linkedin.com/feed/",
            "source": "LinkedIn",
            "date": "Apr 5, 2026",
            "image": "https://placehold.co/600x340/0a66c2/ffffff?text=Mission+Value",
            "tag": "LinkedIn",
            "type": "Post",
        },
        {
            "title": "Digital Transformation Roadmap for GovCon in 2026",
            "summary": "A structured approach to modernizing federal IT infrastructure while maintaining compliance.",
            "link": "https://www.linkedin.com/feed/",
            "source": "LinkedIn",
            "date": "Apr 4, 2026",
            "image": "https://placehold.co/600x340/0a66c2/ffffff?text=GovCon+Digital",
            "tag": "LinkedIn",
            "type": "Post",
        },
    ]