import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
import os
import feedparser

client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
db = client['news_db']
collection = db['articles']

def scrape_forbes():
    """Scrape Forbes RSS feed"""
    try:
        feed = feedparser.parse('https://www.forbes.com/business/feed/')
        articles = []
        for entry in feed.entries[:5]:
            article = {
                'title': entry.title,
                'summary': entry.get('summary', '')[:200],
                'url': entry.link,
                'source': 'Forbes',
                'category': 'Business',
                'image_url': entry.get('media_content', [{}])[0].get('url', ''),
                'date': datetime.utcnow(),
                'scraped_at': datetime.utcnow()
            }
            articles.append(article)
        return articles
    except Exception as e:
        print(f"Forbes error: {e}")
        return []

def scrape_about():
    """Scrape About.com topics"""
    try:
        # Example: Technology section
        url = 'https://www.about.com/topic/technology'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = []
        # Adjust selectors based on actual site structure
        for item in soup.select('.article-card')[:5]:
            article = {
                'title': item.select_one('h2').text if item.select_one('h2') else '',
                'summary': item.select_one('.summary').text[:200] if item.select_one('.summary') else '',
                'url': item.select_one('a')['href'] if item.select_one('a') else '',
                'source': 'About.com',
                'category': 'Technology',
                'image_url': '',
                'date': datetime.utcnow(),
                'scraped_at': datetime.utcnow()
            }
            articles.append(article)
        return articles
    except Exception as e:
        print(f"About.com error: {e}")
        return []

def get_linkedin_news():
    """Use LinkedIn API or RSS (LinkedIn doesn't have public RSS, so use alternative)"""
    # Alternative: Use NewsAPI for LinkedIn-related news
    try:
        api_key = os.getenv('NEWSAPI_KEY')
        url = f'https://newsapi.org/v2/everything?q=LinkedIn&apiKey={api_key}&pageSize=5'
        response = requests.get(url)
        data = response.json()
        
        articles = []
        for item in data.get('articles', [])[:5]:
            article = {
                'title': item['title'],
                'summary': item['description'][:200] if item['description'] else '',
                'url': item['url'],
                'source': 'LinkedIn News',
                'category': 'Professional',
                'image_url': item.get('urlToImage', ''),
                'date': datetime.fromisoformat(item['publishedAt'].replace('Z', '+00:00')),
                'scraped_at': datetime.utcnow()
            }
            articles.append(article)
        return articles
    except Exception as e:
        print(f"LinkedIn error: {e}")
        return []

def run_scrapers():
    """Run all scrapers and save to database"""
    all_articles = []
    
    # Run scrapers
    all_articles.extend(scrape_forbes())
    all_articles.extend(scrape_about())
    all_articles.extend(get_linkedin_news())
    
    # Save to database
    if all_articles:
        collection.insert_many(all_articles)
        print(f"Saved {len(all_articles)} articles")
    
    return all_articles

if __name__ == '__main__':
    run_scrapers()