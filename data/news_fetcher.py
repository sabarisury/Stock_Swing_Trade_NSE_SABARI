"""
News Fetcher for stock market news from multiple sources
"""
import feedparser  # pyright: ignore[reportMissingImports]
import requests
from bs4 import BeautifulSoup  # pyright: ignore[reportMissingModuleSource]
from typing import List, Dict, Optional
import logging
from datetime import datetime, timedelta
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsFetcher:
    """Fetches news from multiple free sources"""
    
    def __init__(self, newsapi_key: Optional[str] = None):
        self.newsapi_key = newsapi_key
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def fetch_newsapi_news(self, query: str, max_results: int = 10) -> List[Dict]:
        """Fetch news from NewsAPI (requires free API key)"""
        articles = []
        
        if not self.newsapi_key:
            logger.warning("NewsAPI key not provided, skipping NewsAPI")
            return articles
        
        try:
            # Global news
            url = f"https://newsapi.org/v2/everything"
            params = {
                'q': query,
                'apiKey': self.newsapi_key,
                'sortBy': 'publishedAt',
                'pageSize': max_results,
                'language': 'en'
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for article in data.get('articles', []):
                    articles.append({
                        'title': article.get('title', ''),
                        'description': article.get('description', ''),
                        'url': article.get('url', ''),
                        'source': article.get('source', {}).get('name', 'NewsAPI'),
                        'published_at': article.get('publishedAt', ''),
                        'content': article.get('content', ''),
                        'type': 'global'
                    })
        except Exception as e:
            logger.error(f"Error fetching NewsAPI news: {str(e)}")
        
        return articles
    
    def fetch_rss_news(self, rss_url: str, max_results: int = 10) -> List[Dict]:
        """Fetch news from RSS feed"""
        articles = []
        try:
            feed = feedparser.parse(rss_url)
            for entry in feed.entries[:max_results]:
                articles.append({
                    'title': entry.get('title', ''),
                    'description': entry.get('description', ''),
                    'url': entry.get('link', ''),
                    'source': feed.feed.get('title', 'RSS Feed'),
                    'published_at': entry.get('published', ''),
                    'content': entry.get('summary', ''),
                    'type': 'rss'
                })
        except Exception as e:
            logger.error(f"Error fetching RSS feed {rss_url}: {str(e)}")
        
        return articles
    def fetch_indian_market_news(self, max_results: int = 20) -> List[Dict]:
        """Fetch Indian market news from RSS feeds"""
        articles = []
        
        # Multiple Indian market RSS feeds
        rss_feeds = [
            'https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms',  # Economic Times Markets
            'https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms',  # Economic Times Stocks
            'https://www.moneycontrol.com/rss/marketreports.xml',  # Moneycontrol Market Reports
            'https://www.business-standard.com/rss/markets-106.rss',  # Business Standard Markets
            'https://www.livemint.com/rss/markets',  # Livemint Markets
        ]
        
        for feed_url in rss_feeds:
            try:
                feed_articles = self.fetch_rss_news(feed_url, max_results // len(rss_feeds))
                for article in feed_articles:
                    article['type'] = 'indian_market'
                articles.extend(feed_articles)
                time.sleep(1)  # Rate limiting
            except Exception as e:
                logger.warning(f"Error fetching Indian market RSS feed {feed_url}: {str(e)}")
                continue  # Continue with next feed if one fails
        
        return articles[:max_results]

    
    def fetch_company_news(self, company_name: str, max_results: int = 15) -> List[Dict]:
        """Fetch company-specific news"""
        articles = []
        
        # Try NewsAPI if key is available
        if self.newsapi_key:
            try:
                newsapi_articles = self.fetch_newsapi_news(f"{company_name} stock India", max_results // 2)
                articles.extend(newsapi_articles)
            except Exception as e:
                logger.error(f"Error fetching company news from NewsAPI: {str(e)}")
        
        # Try scraping Moneycontrol (with rate limiting and error handling)
        try:
            search_url = f"https://www.moneycontrol.com/news/tags/{company_name.lower().replace(' ', '-')}.html"
            # Note: Actual scraping would require more sophisticated handling
            # For now, we'll rely on RSS and NewsAPI
        except Exception as e:
            logger.warning(f"Could not scrape company news: {str(e)}")
        
        return articles[:max_results]
    
    def fetch_global_market_news(self, max_results: int = 15) -> List[Dict]:
        """Fetch global market news"""
        articles = []
        
        if self.newsapi_key:
            try:
                newsapi_articles = self.fetch_newsapi_news("stock market global economy", max_results)
                articles.extend(newsapi_articles)
            except Exception as e:
                logger.error(f"Error fetching global market news: {str(e)}")
        
        # Add RSS feeds for global markets (multiple alternatives)
        global_rss = [
            'https://feeds.finance.yahoo.com/rss/2.0/headline?s=%5EGSPC&region=US&lang=en-US',  # Yahoo Finance - S&P 500
            'https://feeds.finance.yahoo.com/rss/2.0/headline?s=%5EDJI&region=US&lang=en-US',  # Yahoo Finance - Dow Jones
            'http://feeds.marketwatch.com/marketwatch/marketpulse/',  # MarketWatch
            'https://www.cnbc.com/id/100003114/device/rss/rss.html',  # CNBC Business
            'https://feeds.bbci.co.uk/news/business/rss.xml',  # BBC Business
        ]
        
        for feed_url in global_rss:
            try:
                feed_articles = self.fetch_rss_news(feed_url, max_results // len(global_rss))
                for article in feed_articles:
                    article['type'] = 'global_market'
                articles.extend(feed_articles)
                time.sleep(1)  # Rate limiting
            except Exception as e:
                logger.warning(f"Error fetching global RSS feed {feed_url}: {str(e)}")
                continue  # Continue with next feed if one fails
        
        return articles[:max_results]
    

    
    def get_all_news(self, company_name: str, stock_symbol: str, max_per_source: int = 10) -> Dict:
        """Get all news: global, Indian market, and company-specific"""
        all_news = {
            'global_news': self.fetch_global_market_news(max_per_source),
            'indian_market_news': self.fetch_indian_market_news(max_per_source),
            'company_news': self.fetch_company_news(company_name, max_per_source),
        }
        
        return all_news
    
    def format_news_for_analysis(self, news_dict: Dict) -> str:
        """Format news articles into a single text for sentiment analysis"""
        formatted_text = []
        
        for news_type, articles in news_dict.items():
            formatted_text.append(f"\n=== {news_type.upper().replace('_', ' ')} ===\n")
            for article in articles:
                formatted_text.append(f"Title: {article.get('title', '')}")
                formatted_text.append(f"Description: {article.get('description', '')}")
                formatted_text.append(f"Source: {article.get('source', '')}")
                formatted_text.append("---\n")
        
        return "\n".join(formatted_text)

