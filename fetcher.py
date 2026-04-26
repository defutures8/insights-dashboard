import feedparser
import re

FEEDS = {
    "Forbes": "https://www.forbes.com/innovation/feed/",
    "Forbes Business": "https://www.forbes.com/business/feed/",
    "MIT Tech Review": "https://www.technologyreview.com/feed/",
    "Harvard Business Review": "https://feeds.hbr.org/harvardbusiness",
    "VentureBeat": "https://venturebeat.com/feed/",
    "TechCrunch": "https://techcrunch.com/feed/",
}

FALLBACK_IMAGES = {
    "Forbes": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&h=340&fit=crop",
    "MIT": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&h=340&fit=crop",
    "Harvard": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=600&h=340&fit=crop",
    "VentureBeat": "https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=600&h=340&fit=crop",
    "TechCrunch": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=600&h=340&fit=crop",
    "LinkedIn": "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=600&h=340&fit=crop",
    "YouTube": "https://images.unsplash.com/photo-1611162616475-46b635cb6868?w=600&h=340&fit=crop",
}

BLOCKLIST = [
    "Wordle", "Quordle", "Strands", "NYT", "crossword", "puzzle",
    "Hints", "Clues", "Answers Today",
    "WWE", "NFL", "NBA", "MLB", "UFC",
    "celebrity", "Celebrity",
    "movie", "Movie", "Netflix", "Disney",
    "TV show", "sitcom", "comedian",
    "Invincible", "Marvel", "DC Comics",
    "music", "album", "singer", "rapper",
    "Grammy", "Oscar", "Emmy",
    "shark", "Shark", "whale", "dolphin",
    "AstroTurf", "fake grass",
    "Desalination", "Download:",
    "Super Bowl", "World Series", "March Madness",
    "quarterback", "touchdown", "home run",
    "video game", "Video Game", "Xbox", "PlayStation",
    "Minecraft", "Fortnite", "Nintendo",
    "MacBook", "iPhone", "iPad", "Apple Watch",
]

PINNED_ARTICLES = [
    {
        "title": "The US Government Is Headed For Disruptive Digital Transformation in 2026",
        "summary": "Federal agencies are scaling AI to modernize operations, enhance decision-making and improve mission outcomes. From defense to diplomacy, AI is emerging as a foundational pillar of digital transformation strategies across government...",
        "link": "https://fedscoop.com/federal-government-digital-transformation-2026/",
        "source": "FedScoop",
        "date": "Jan 9, 2026",
        "image": "https://images.unsplash.com/photo-1523437113738-bbd3cc89fb19?w=800&h=480&fit=crop",
        "tag": "Federal AI",
        "type": "Report",
    },
]

PINNED_THREE_COL = [
  {
        "title": "Three reasons why DeepSeek's new model matters",
        "summary": "DeepSeek's latest model is turning heads across the AI industry. Here are three reasons why it represents a significant shift in the competitive landscape...",
        "link": "https://www.technologyreview.com/",
        "source": "MIT Tech Review",
        "date": "Apr 2026",
        "image": "https://images.unsplash.com/photo-1677442135703-1787eea5ce01?w=600&h=340&fit=crop",
        "tag": "MIT Review",
        "type": "Article",
    },
    {
        "title": "If You See This Microsoft Login—Your Account Is Being Hacked",
        "summary": "Do not sign-in on this page — it's an attack and your account will be hijacked. Here is how to spot it and protect yourself...",
        "link": "https://www.forbes.com/sites/forbestechcouncil/",
        "source": "Forbes",
        "date": "Sun, 19 Apr 2026",
        "image": "https://images.unsplash.com/photo-1633419461186-7d40a38105ec?w=600&h=340&fit=crop",
        "tag": "Forbes",
        "type": "Article",
    },
    {
        "title": "Anthropic created a test marketplace for agent-on-agent commerce",
        "summary": "Anthropic has launched a marketplace designed to let AI agents transact with each other, marking a significant step toward autonomous agent-based economies...",
        "link": "https://techcrunch.com/",
        "source": "TechCrunch",
        "date": "Apr 2026",
        "image": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=600&h=340&fit=crop",
        "tag": "TechCrunch",
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
    import random
    pinned = list(PINNED_ARTICLES)
    articles = []
    for source, url in FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:8]:
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
                    "tag": source.replace(" Tech", "").replace(" AI", "").replace(" Business", ""),
                    "type": "Article",
                })
        except Exception as e:
            print(f"Feed error for {source}: {e}")
    random.shuffle(articles)
    return pinned + articles

def get_hero_article():
    return get_all_articles()[0]

def get_recommended():
    return get_all_articles()[1:5]

def get_three_col():
    if PINNED_THREE_COL:
        return PINNED_THREE_COL
    return get_all_articles()[1:4]

def get_four_col():
    return get_all_articles()[7:11]

def get_articles():
    return get_all_articles()[:9]

def get_linkedin_posts():
    return [
        {
            "title": "From Authorization to Actualization: Where Mission Value Breaks Down",
            "summary": "Initiatives start with intent, but seems to lose value in execution across the lifecycle.",
            "link": "https://www.linkedin.com/feed/",
            "source": "LinkedIn",
            "date": "Apr 5, 2026",
            "image": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=600&h=340&fit=crop",
            "tag": "LinkedIn",
            "type": "Blog",
        },
        {
            "title": "From Investment to Impact: Why Orchestration Matters",
            "summary": "Across enterprise and government, outcomes  don't follow investment, but orchestration.",
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

def get_youtube_posts():
    return [
        {
            "title": "Chaos is Opportunity in GovCon",
            "summary": "Chaos, Capture and Money - Neil McDonnell, GovCon chamber of commerce founder, Best8a.com Interview",
            "link": "https://www.youtube.com/watch?v=lsWUiMhYhSc",
            "source": "YouTube",
            "date": "2026",
            "image": "https://img.youtube.com/vi/lsWUiMhYhSc/maxresdefault.jpg",
            "tag": "YouTube",
            "type": "Video",
        },
    
    ]