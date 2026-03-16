import feedparser
import requests
from datetime import datetime

FEEDS = {
    "Forbes AI": "https://www.forbes.com/innovation/feed/",
    "Forbes Finance": "https://www.forbes.com/money/feed/",
    "MIT Tech Review": "https://www.technologyreview.com/feed/",
    "Harvard Business Review": "https://feeds.hbr.org/harvardbusiness",
}

def get_articles(limit=12):
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
                    "date": entry.get("published", ""),
                    "image": extract_image(entry),
                    "tag": source.split()[0],
                })
        except Exception as e:
            print(f"Feed error for {source}: {e}")
    return articles[:limit]

def extract_image(entry):
    # Try media_thumbnail first, then media_content
    if hasattr(entry, "media_thumbnail"):
        return entry.media_thumbnail[0].get("url", "")
    if hasattr(entry, "media_content"):
        return entry.media_content[0].get("url", "")
    return "https://placehold.co/400x220/1a1a2e/fff?text=Insight"