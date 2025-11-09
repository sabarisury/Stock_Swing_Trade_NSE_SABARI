"""
API Validation Script - Tests all APIs used in the system
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import yfinance as yf
import feedparser
import requests
from datetime import datetime

def test_yfinance_api():
    """Test yfinance API for NSE stocks"""
    print("=" * 60)
    print("Testing yfinance API (Stock Data)")
    print("=" * 60)
    
    test_symbols = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]
    
    for symbol in test_symbols:
        try:
            print(f"\n📊 Testing {symbol}...")
            ticker = yf.Ticker(symbol)
            
            # Test 1: Get info
            try:
                info = ticker.info
                print(f"   ✅ Info fetched: {info.get('longName', 'N/A')}")
            except Exception as e:
                print(f"   ❌ Info failed: {str(e)}")
            
            # Test 2: Get current price
            try:
                data = ticker.history(period="5d")
                if not data.empty:
                    current_price = data['Close'].iloc[-1]
                    print(f"   ✅ Current price: ₹{current_price:.2f}")
                else:
                    print(f"   ⚠️  No price data returned")
            except Exception as e:
                print(f"   ❌ Price fetch failed: {str(e)}")
            
            # Test 3: Get historical data (1 year)
            try:
                hist_data = ticker.history(period="1y")
                if not hist_data.empty:
                    print(f"   ✅ Historical data: {len(hist_data)} days")
                    print(f"      Date range: {hist_data.index[0].date()} to {hist_data.index[-1].date()}")
                    print(f"      Columns: {list(hist_data.columns)}")
                    
                    # Check if we have required columns
                    required = ['Open', 'High', 'Low', 'Close']
                    missing = [col for col in required if col not in hist_data.columns]
                    if missing:
                        print(f"   ⚠️  Missing columns: {missing}")
                    else:
                        print(f"   ✅ All required columns present")
                else:
                    print(f"   ❌ No historical data returned")
            except Exception as e:
                print(f"   ❌ Historical data failed: {str(e)}")
            
            # Test 4: Get fundamental data
            try:
                info = ticker.info
                pe = info.get('trailingPE')
                pb = info.get('priceToBook')
                roe = info.get('returnOnEquity')
                print(f"   ✅ Fundamental data: P/E={pe}, P/B={pb}, ROE={roe}")
            except Exception as e:
                print(f"   ❌ Fundamental data failed: {str(e)}")
                
        except Exception as e:
            print(f"   ❌ Overall test failed for {symbol}: {str(e)}")
    
    print("\n" + "=" * 60)


def test_rss_feeds():
    """Test RSS feeds for news"""
    print("=" * 60)
    print("Testing RSS Feeds (News)")
    print("=" * 60)
    
    rss_feeds = [
        ('Economic Times Markets', 'https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms'),
        ('Economic Times Stocks', 'https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms'),
        ('Reuters Business', 'https://feeds.reuters.com/reuters/businessNews'),
    ]
    
    for name, url in rss_feeds:
        try:
            print(f"\n📰 Testing {name}...")
            print(f"   URL: {url}")
            
            feed = feedparser.parse(url)
            
            if feed.bozo:
                print(f"   ⚠️  Feed parsing warning: {feed.bozo_exception}")
            
            if len(feed.entries) > 0:
                print(f"   ✅ Feed working: {len(feed.entries)} articles found")
                print(f"      Latest: {feed.entries[0].get('title', 'N/A')[:60]}...")
                print(f"      Published: {feed.entries[0].get('published', 'N/A')}")
            else:
                print(f"   ⚠️  Feed accessible but no articles found")
                
        except Exception as e:
            print(f"   ❌ Feed failed: {str(e)}")
    
    print("\n" + "=" * 60)


def test_newsapi():
    """Test NewsAPI if key is provided"""
    print("=" * 60)
    print("Testing NewsAPI")
    print("=" * 60)
    
    api_key = os.environ.get('NEWSAPI_KEY') or input("Enter NewsAPI key (or press Enter to skip): ").strip()
    
    if not api_key:
        print("⚠️  No NewsAPI key provided. Skipping NewsAPI test.")
        print("   (This is optional - RSS feeds will be used instead)")
        return
    
    try:
        print(f"\n🔑 Testing NewsAPI with key: {api_key[:10]}...")
        
        # Test global news
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': 'stock market',
            'apiKey': api_key,
            'sortBy': 'publishedAt',
            'pageSize': 5,
            'language': 'en'
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            print(f"   ✅ NewsAPI working: {len(articles)} articles found")
            if articles:
                print(f"      Latest: {articles[0].get('title', 'N/A')[:60]}...")
        elif response.status_code == 401:
            print(f"   ❌ Invalid API key")
        elif response.status_code == 429:
            print(f"   ⚠️  Rate limit exceeded (free tier: 100 requests/day)")
        else:
            print(f"   ❌ Error {response.status_code}: {response.text[:100]}")
            
    except Exception as e:
        print(f"   ❌ NewsAPI test failed: {str(e)}")
    
    print("\n" + "=" * 60)


def test_technical_analysis_library():
    """Test if technical analysis library works"""
    print("=" * 60)
    print("Testing Technical Analysis Library")
    print("=" * 60)
    
    try:
        import ta
        import pandas as pd
        import numpy as np
        
        print("\n📈 Testing TA library...")
        
        # Create sample data
        dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
        sample_data = pd.DataFrame({
            'Open': np.random.randn(100).cumsum() + 100,
            'High': np.random.randn(100).cumsum() + 105,
            'Low': np.random.randn(100).cumsum() + 95,
            'Close': np.random.randn(100).cumsum() + 100,
            'Volume': np.random.randint(1000000, 5000000, 100)
        }, index=dates)
        
        # Test RSI
        try:
            rsi = ta.momentum.RSIIndicator(sample_data['Close'], window=14)
            rsi_value = rsi.rsi().iloc[-1]
            print(f"   ✅ RSI calculation: {rsi_value:.2f}")
        except Exception as e:
            print(f"   ❌ RSI failed: {str(e)}")
        
        # Test MACD
        try:
            macd = ta.trend.MACD(sample_data['Close'])
            macd_value = macd.macd().iloc[-1]
            print(f"   ✅ MACD calculation: {macd_value:.4f}")
        except Exception as e:
            print(f"   ❌ MACD failed: {str(e)}")
        
        # Test SMA
        try:
            sma = ta.trend.SMAIndicator(sample_data['Close'], window=20)
            sma_value = sma.sma_indicator().iloc[-1]
            print(f"   ✅ SMA calculation: {sma_value:.2f}")
        except Exception as e:
            print(f"   ❌ SMA failed: {str(e)}")
        
        # Test Bollinger Bands
        try:
            bb = ta.volatility.BollingerBands(sample_data['Close'], window=20)
            bb_upper = bb.bollinger_hband().iloc[-1]
            print(f"   ✅ Bollinger Bands: Upper={bb_upper:.2f}")
        except Exception as e:
            print(f"   ❌ Bollinger Bands failed: {str(e)}")
        
        # Test Stochastic
        try:
            stoch = ta.momentum.StochasticOscillator(
                sample_data['High'], 
                sample_data['Low'], 
                sample_data['Close'], 
                window=14
            )
            stoch_k = stoch.stoch().iloc[-1]
            print(f"   ✅ Stochastic: %K={stoch_k:.2f}")
        except Exception as e:
            print(f"   ❌ Stochastic failed: {str(e)}")
        
        print("   ✅ Technical Analysis library is working!")
        
    except ImportError as e:
        print(f"   ❌ TA library not installed: {str(e)}")
        print("   Run: pip install ta")
    except Exception as e:
        print(f"   ❌ TA library test failed: {str(e)}")
    
    print("\n" + "=" * 60)


def test_sentiment_libraries():
    """Test sentiment analysis libraries"""
    print("=" * 60)
    print("Testing Sentiment Analysis Libraries")
    print("=" * 60)
    
    # Test VADER
    try:
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        analyzer = SentimentIntensityAnalyzer()
        test_text = "The stock market is performing very well today!"
        scores = analyzer.polarity_scores(test_text)
        print(f"\n✅ VADER Sentiment working")
        print(f"   Test: '{test_text}'")
        print(f"   Score: {scores['compound']:.2f} (compound)")
    except ImportError:
        print(f"\n❌ VADER Sentiment not installed")
        print("   Run: pip install vaderSentiment")
    except Exception as e:
        print(f"\n❌ VADER Sentiment failed: {str(e)}")
    
    # Test TextBlob
    try:
        from textblob import TextBlob
        test_text = "The company reported excellent quarterly results"
        blob = TextBlob(test_text)
        polarity = blob.sentiment.polarity
        print(f"\n✅ TextBlob Sentiment working")
        print(f"   Test: '{test_text}'")
        print(f"   Polarity: {polarity:.2f}")
    except ImportError:
        print(f"\n❌ TextBlob not installed")
        print("   Run: pip install textblob")
    except Exception as e:
        print(f"\n❌ TextBlob failed: {str(e)}")
    
    print("\n" + "=" * 60)


def main():
    """Run all API tests"""
    print("\n" + "=" * 60)
    print("API VALIDATION TEST SUITE")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all tests
    test_yfinance_api()
    test_rss_feeds()
    test_newsapi()
    test_technical_analysis_library()
    test_sentiment_libraries()
    
    print("\n" + "=" * 60)
    print("VALIDATION COMPLETE")
    print("=" * 60)
    print("\nSummary:")
    print("- Check above for any ❌ errors")
    print("- All ✅ means APIs are working")
    print("- ⚠️  warnings indicate partial functionality")
    print()


if __name__ == "__main__":
    main()