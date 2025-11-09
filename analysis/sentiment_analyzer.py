"""
Sentiment Analysis Module for news articles
"""
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """Analyzes sentiment from news articles"""
    
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
    
    def analyze_sentiment_vader(self, text: str) -> Dict:
        """Analyze sentiment using VADER"""
        try:
            scores = self.vader_analyzer.polarity_scores(text)
            return {
                'compound': scores['compound'],
                'positive': scores['pos'],
                'neutral': scores['neu'],
                'negative': scores['neg'],
                'method': 'vader'
            }
        except Exception as e:
            logger.error(f"Error in VADER sentiment analysis: {str(e)}")
            return {'compound': 0.0, 'method': 'vader'}
    
    def analyze_sentiment_textblob(self, text: str) -> Dict:
        """Analyze sentiment using TextBlob"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            return {
                'polarity': polarity,
                'subjectivity': subjectivity,
                'method': 'textblob'
            }
        except Exception as e:
            logger.error(f"Error in TextBlob sentiment analysis: {str(e)}")
            return {'polarity': 0.0, 'method': 'textblob'}
    
    def analyze_article(self, article: Dict) -> Dict:
        """Analyze sentiment of a single article"""
        try:
            # Combine title and description for analysis
            text = f"{article.get('title', '')} {article.get('description', '')}"
            
            vader_result = self.analyze_sentiment_vader(text)
            textblob_result = self.analyze_sentiment_textblob(text)
            
            # Combine results
            combined_score = (vader_result['compound'] + textblob_result['polarity']) / 2
            
            return {
                'article_title': article.get('title', ''),
                'source': article.get('source', ''),
                'vader_score': vader_result['compound'],
                'textblob_score': textblob_result['polarity'],
                'combined_score': combined_score,
                'sentiment': self._classify_sentiment(combined_score),
                'type': article.get('type', 'unknown')
            }
        except Exception as e:
            logger.error(f"Error analyzing article: {str(e)}")
            return {'sentiment': 'NEUTRAL', 'combined_score': 0.0}
    
    def analyze_news_collection(self, news_dict: Dict) -> Dict:
        """Analyze sentiment for all news collections"""
        results = {
            'global_news': {'articles': [], 'average_sentiment': 0.0, 'count': 0},
            'indian_market_news': {'articles': [], 'average_sentiment': 0.0, 'count': 0},
            'company_news': {'articles': [], 'average_sentiment': 0.0, 'count': 0},
            'overall_sentiment': 0.0,
            'sentiment_breakdown': {}
        }
        
        try:
            total_sentiment = 0.0
            total_count = 0
            
            for news_type, articles in news_dict.items():
                if not articles:
                    continue
                
                type_sentiments = []
                analyzed_articles = []
                
                for article in articles:
                    analysis = self.analyze_article(article)
                    analyzed_articles.append(analysis)
                    type_sentiments.append(analysis['combined_score'])
                
                if type_sentiments:
                    avg_sentiment = sum(type_sentiments) / len(type_sentiments)
                    results[news_type] = {
                        'articles': analyzed_articles,
                        'average_sentiment': avg_sentiment,
                        'count': len(analyzed_articles),
                        'sentiment_label': self._classify_sentiment(avg_sentiment)
                    }
                    
                    total_sentiment += avg_sentiment * len(type_sentiments)
                    total_count += len(type_sentiments)
            
            if total_count > 0:
                results['overall_sentiment'] = total_sentiment / total_count
                results['overall_sentiment_label'] = self._classify_sentiment(results['overall_sentiment'])
            
            # Sentiment breakdown
            results['sentiment_breakdown'] = {
                'very_positive': sum(1 for r in results.values() if isinstance(r, dict) and r.get('average_sentiment', 0) > 0.5),
                'positive': sum(1 for r in results.values() if isinstance(r, dict) and 0.1 < r.get('average_sentiment', 0) <= 0.5),
                'neutral': sum(1 for r in results.values() if isinstance(r, dict) and -0.1 <= r.get('average_sentiment', 0) <= 0.1),
                'negative': sum(1 for r in results.values() if isinstance(r, dict) and -0.5 <= r.get('average_sentiment', 0) < -0.1),
                'very_negative': sum(1 for r in results.values() if isinstance(r, dict) and r.get('average_sentiment', 0) < -0.5),
            }
            
        except Exception as e:
            logger.error(f"Error analyzing news collection: {str(e)}")
        
        return results
    
    def _classify_sentiment(self, score: float) -> str:
        """Classify sentiment score into label"""
        if score >= 0.5:
            return 'VERY_POSITIVE'
        elif score >= 0.1:
            return 'POSITIVE'
        elif score >= -0.1:
            return 'NEUTRAL'
        elif score >= -0.5:
            return 'NEGATIVE'
        else:
            return 'VERY_NEGATIVE'
    
    def get_sentiment_score_for_prediction(self, sentiment_results: Dict) -> float:
        """Get a normalized sentiment score (-100 to +100) for prediction"""
        overall = sentiment_results.get('overall_sentiment', 0.0)
        # Normalize from [-1, 1] to [-100, 100]
        return overall * 100

