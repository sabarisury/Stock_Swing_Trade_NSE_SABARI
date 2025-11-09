"""
CrewAI Crew Configuration with Supervisor
"""
# Make CrewAI imports optional
try:
    from crewai import Crew, Process  # pyright: ignore[reportMissingImports]
    from agents.stock_agents import (
        create_data_collector_agent,
        create_technical_analysis_agent,
        create_fundamental_analysis_agent,
        create_sentiment_analysis_agent,
        create_prediction_agent,
        create_supervisor_agent,
        create_data_collection_task,
        create_technical_analysis_task,
        create_fundamental_analysis_task,
        create_sentiment_analysis_task,
        create_prediction_task,
        create_supervision_task
    )
    CREWAI_AVAILABLE = True
except Exception as e:
    CREWAI_AVAILABLE = False
    import logging
    logging.warning(f"CrewAI not available: {e}. Running without CrewAI agents.")

from data.stock_fetcher import StockFetcher
from data.news_fetcher import NewsFetcher
from analysis.technical_analyzer import TechnicalAnalyzer
from analysis.fundamental_analyzer import FundamentalAnalyzer
from analysis.sentiment_analyzer import SentimentAnalyzer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StockAnalysisCrew:
    """CrewAI crew for stock market analysis"""
    
    def __init__(self, newsapi_key: str = None, use_crewai: bool = False):
        self.stock_fetcher = StockFetcher()
        self.news_fetcher = NewsFetcher(newsapi_key=newsapi_key)
        self.technical_analyzer = TechnicalAnalyzer()
        self.fundamental_analyzer = FundamentalAnalyzer()
        self.sentiment_analyzer = SentimentAnalyzer()
        
        # Only create agents if CrewAI is available and requested
        self.agents_available = False
        if use_crewai and CREWAI_AVAILABLE:
            try:
                # Create agents (only if API key is set)
                self.data_collector = create_data_collector_agent()
                self.technical_agent = create_technical_analysis_agent()
                self.fundamental_agent = create_fundamental_analysis_agent()
                self.sentiment_agent = create_sentiment_analysis_agent()
                self.prediction_agent = create_prediction_agent()
                self.supervisor = create_supervisor_agent()
                self.agents_available = True
                logger.info("CrewAI agents initialized successfully")
            except Exception as e:
                logger.warning(f"Could not initialize CrewAI agents: {e}. Continuing without agents.")
                self.agents_available = False
                
        else:
            logger.info("Running without CrewAI agents (using direct analyzers)")
    
    def analyze_stock(self, stock_symbol: str, time_horizon_weeks: int = 2) -> dict:
        """
        Main method to analyze a stock using the crew
        
        Args:
            stock_symbol: NSE stock symbol (e.g., 'RELIANCE' or 'RELIANCE.NS')
            time_horizon_weeks: Time horizon for swing trading (1-4 weeks)
        
        Returns:
            Dictionary with complete analysis and recommendation
        """
        try:
            # Step 1: Collect data (outside crew for now, as crew agents need tools)
            logger.info(f"Fetching data for {stock_symbol}...")
            stock_data = self.stock_fetcher.get_all_data(stock_symbol, period="1y")
            
            if not stock_data.get('current_price'):
                return {'error': f'Could not fetch data for {stock_symbol}. Please check the symbol.'}
            
            company_name = stock_data['info'].get('name', stock_symbol)
            historical_data = stock_data['historical_data']
            fundamental_data = stock_data['fundamental_data']
            
            # Step 2: Perform analyses (using our analyzers directly)
            logger.info("Performing technical analysis...")
            technical_indicators = self.technical_analyzer.calculate_indicators(historical_data)
            technical_signals = self.technical_analyzer.generate_signals(technical_indicators)
            technical_analysis = {
                'indicators': technical_indicators,
                'signals': technical_signals
            }
            
            logger.info("Performing fundamental analysis...")
            fundamental_analysis = self.fundamental_analyzer.analyze_fundamentals(fundamental_data)
            
            logger.info("Fetching and analyzing news sentiment...")
            all_news = self.news_fetcher.get_all_news(company_name, stock_symbol, max_per_source=10)
            sentiment_analysis = self.sentiment_analyzer.analyze_news_collection(all_news)
            
            # Step 3: Create tasks for CrewAI agents
            # Note: For now, we'll use the analyzers directly, but structure it for CrewAI integration
            # In a full CrewAI implementation, agents would use tools to call these analyzers
            
            # Step 4: Generate prediction (using our predictor)
            from prediction.trading_predictor import TradingPredictor  # pyright: ignore[reportMissingImports]
            predictor = TradingPredictor()
            recommendation = predictor.generate_recommendation(
                stock_symbol=stock_symbol,
                current_price=stock_data['current_price'],
                time_horizon_weeks=time_horizon_weeks,
                technical_analysis=technical_analysis,
                fundamental_analysis=fundamental_analysis,
                sentiment_analysis=sentiment_analysis,
                historical_data=historical_data
            )
            
            # Step 5: Compile results
            results = {
                'stock_info': stock_data['info'],
                'current_price': stock_data['current_price'],
                'technical_analysis': technical_analysis,
                'fundamental_analysis': fundamental_analysis,
                'sentiment_analysis': sentiment_analysis,
                'recommendation': recommendation,
                'news_summary': {
                    'global_news_count': len(all_news.get('global_news', [])),
                    'indian_news_count': len(all_news.get('indian_market_news', [])),
                    'company_news_count': len(all_news.get('company_news', []))
                }
            }
            
            logger.info("Analysis complete!")
            return results
            
        except Exception as e:
            logger.error(f"Error in stock analysis: {str(e)}")
            return {'error': f'Analysis failed: {str(e)}'}


def create_crew_with_tools():
    """
    Creates a CrewAI crew with proper tool integration
    Note: This is a placeholder for full CrewAI implementation with tools
    """
    # For now, we use the StockAnalysisCrew class which handles everything
    # In a full implementation, agents would have tools to call the analyzers
    pass