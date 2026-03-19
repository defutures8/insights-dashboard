import feedparser
import requests
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
    return "https://placehold.co/400x220/1a1a2e/fff?text=Insight"

def get_articles(limit=9):
    articles = []
    for source, url in FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]:
                articles.append({
                    "title": entry.get("title", "Untitled"),
                    "summary": entry.get("summary", "")[:160] + "...",
                    "link": entry.get("link", "#"),
                    "source": source,
                    "date": entry.get("published", "")[:16] if entry.get("published") else "",
                    "image": extract_image(entry),
                    "tag": source.split()[0],
                })
        except Exception as e:
            print(f"Feed error for {source}: {e}")
    return articles[:limit]

def get_linkedin_posts():
    return [
        {
            "title": "Why AI Governance is the #1 Priority for Federal Contractors in 2026",
            "summary": "Organizations that build trust through transparent AI frameworks are winning more contracts. Here is what the top performers are doing differently this year.",
            "link": "https://www.linkedin.com/feed/",
            "source": "LinkedIn",
            "date": "Wed, 18 Mar 2026",
            "image": "https://placehold.co/400x220/0a66c2/ffffff?text=AI+Governance",
            "tag": "LinkedIn",
        },
        {
            "title": "The 5 AI Skills Federal Agencies Are Hiring For Right Now",
            "summary": "From prompt engineering to ATO acceleration, agencies are moving fast. These are the capabilities that matter most heading into Q2 2026.",
            "link": "https://www.linkedin.com/feed/",
            "source": "LinkedIn",
            "date": "Tue, 17 Mar 2026",
            "image": "https://placehold.co/400x220/0a66c2/ffffff?text=Federal+AI",
            "tag": "LinkedIn",
        },
        {
            "title": "Mission Value Orchestration: From Authorization to Actualization",
            "summary": "The firms closing the gap between ATO approval and real operational value are using a structured orchestration approach. Here is the framework that works.",
            "link": "https://www.linkedin.com/feed/",
            "source": "LinkedIn",
            "date": "Mon, 16 Mar 2026",
            "image": "https://placehold.co/400x220/0a66c2/ffffff?text=Mission+Value",
            "tag": "LinkedIn",
        },
    ]