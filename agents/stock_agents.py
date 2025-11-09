"""
CrewAI Agents for Stock Market Analysis
"""
from crewai import Agent  # pyright: ignore[reportMissingImports]
from crewai import Task  # pyright: ignore[reportMissingImports]
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.stock_fetcher import StockFetcher
from data.news_fetcher import NewsFetcher
from analysis.technical_analyzer import TechnicalAnalyzer
from analysis.fundamental_analyzer import FundamentalAnalyzer
from analysis.sentiment_analyzer import SentimentAnalyzer


def create_data_collector_agent() -> Agent:
    """Creates the Data Collector Agent"""
    return Agent(
        role='Stock Data Collector',
        goal='Fetch real-time stock price, historical data, and company information for NSE stocks',
        backstory="""You are an expert data collector specializing in Indian stock market (NSE) data.
        You have access to real-time market data and can fetch comprehensive stock information including
        current prices, historical data, and fundamental metrics. You ensure data accuracy and completeness.""",
        verbose=True,
        allow_delegation=False,
    )


def create_technical_analysis_agent() -> Agent:
    """Creates the Technical Analysis Agent"""
    return Agent(
        role='Technical Analysis Specialist',
        goal='Analyze stock price patterns, trends, and technical indicators to identify trading opportunities',
        backstory="""You are a seasoned technical analyst with expertise in reading charts and technical indicators.
        You analyze price movements, volume patterns, momentum indicators (RSI, MACD), trend indicators (Moving Averages),
        volatility indicators (Bollinger Bands, ATR), and support/resistance levels. You provide clear technical signals
        for swing trading decisions.""",
        verbose=True,
        allow_delegation=False,
    )


def create_fundamental_analysis_agent() -> Agent:
    """Creates the Fundamental Analysis Agent"""
    return Agent(
        role='Fundamental Analysis Expert',
        goal='Evaluate company financial health, valuation metrics, and business fundamentals',
        backstory="""You are a financial analyst specializing in fundamental analysis of Indian companies.
        You evaluate financial ratios (P/E, P/B, Debt-to-Equity), profitability metrics (ROE, ROA, margins),
        growth metrics (revenue growth, earnings growth), and liquidity ratios. You assess whether a stock
        is fundamentally strong and fairly valued for swing trading.""",
        verbose=True,
        allow_delegation=False,
    )


def create_sentiment_analysis_agent() -> Agent:
    """Creates the Sentiment Analysis Agent"""
    return Agent(
        role='Market Sentiment Analyst',
        goal='Analyze news sentiment from global, Indian market, and company-specific sources',
        backstory="""You are a sentiment analysis expert who monitors news from multiple sources including
        global financial news, Indian market news, and company-specific announcements. You use NLP techniques
        to assess market sentiment and determine how news might impact stock prices. You provide sentiment scores
        that help predict short-term price movements for swing trading.""",
        verbose=True,
        allow_delegation=False,
    )


def create_prediction_agent() -> Agent:
    """Creates the Prediction Agent"""
    return Agent(
        role='Trading Prediction Specialist',
        goal='Synthesize technical, fundamental, and sentiment analysis to generate swing trading recommendations',
        backstory="""You are an expert trading strategist who combines multiple analysis perspectives to make
        informed swing trading decisions. You weigh technical signals, fundamental strength, and market sentiment
        to provide actionable recommendations with confidence scores, target prices, stop-loss levels, and risk assessments.
        You specialize in 1-4 week swing trading strategies for Indian stocks.""",
        verbose=True,
        allow_delegation=False,
    )


def create_supervisor_agent() -> Agent:
    """Creates the Supervisor Agent"""
    return Agent(
        role='Analysis Supervisor and Quality Controller',
        goal='Validate all agent outputs, ensure data quality, check consistency, and coordinate the analysis workflow',
        backstory="""You are a senior analyst and quality controller overseeing the entire stock analysis process.
        You ensure that all agents perform their tasks correctly, validate the data quality, check for consistency
        across different analyses, and ensure the final recommendation is well-supported by evidence. You catch errors
        and ensure the analysis meets high standards before presenting to users.""",
        verbose=True,
        allow_delegation=True,
    )


def create_data_collection_task(agent: Agent, stock_symbol: str) -> Task:
    """Creates task for data collection"""
    return Task(
        description=f"""
        Collect comprehensive stock data for {stock_symbol}:
        1. Fetch current/latest stock price
        2. Get historical price data (at least 1 year)
        3. Retrieve company information (name, sector, industry, market cap)
        4. Extract fundamental/financial metrics (P/E, P/B, ROE, ROA, margins, growth rates, etc.)
        5. Ensure all data is real-time and accurate
        
        Return a structured summary with:
        - Current price
        - Company name and sector
        - Historical data summary
        - All available fundamental metrics
        """,
        agent=agent,
        expected_output="A comprehensive data summary including current price, company info, historical data summary, and fundamental metrics in a structured format"
    )


def create_technical_analysis_task(agent: Agent, stock_symbol: str, historical_data) -> Task:
    """Creates task for technical analysis"""
    return Task(
        description=f"""
        Perform comprehensive technical analysis for {stock_symbol}:
        1. Calculate at least 15 technical indicators including:
           - Moving Averages (SMA 20, 50, 200; EMA 12, 26)
           - Momentum indicators (RSI, MACD, Stochastic, Williams %R, ROC, PPO)
           - Volatility indicators (Bollinger Bands, ATR)
           - Volume indicators (Volume ratio, OBV)
           - Trend indicators (ADX, CCI)
           - Support and Resistance levels
        2. Identify current trend (uptrend, downtrend, sideways)
        3. Generate trading signals (buy, sell, hold) with reasoning
        4. Assess signal strength
        
        Use the provided historical price data to calculate all indicators.
        """,
        agent=agent,
        expected_output="A detailed technical analysis report with all calculated indicators, trend assessment, trading signals, and signal strength"
    )


def create_fundamental_analysis_task(agent: Agent, stock_symbol: str, fundamental_data) -> Task:
    """Creates task for fundamental analysis"""
    return Task(
        description=f"""
        Perform comprehensive fundamental analysis for {stock_symbol}:
        1. Analyze at least 10 fundamental metrics including:
           - Valuation ratios (P/E, Forward P/E, P/B, PEG)
           - Profitability (ROE, ROA, Profit Margin, Operating Margin)
           - Growth metrics (Revenue Growth, Earnings Growth)
           - Financial health (Debt-to-Equity, Current Ratio, Quick Ratio)
           - Market metrics (Beta, Dividend Yield)
        2. Score each metric and provide overall fundamental strength assessment
        3. Identify strengths and weaknesses
        4. Determine if stock is fundamentally sound for swing trading
        
        Use the provided fundamental data to perform the analysis.
        """,
        agent=agent,
        expected_output="A comprehensive fundamental analysis report with metric scores, overall assessment, strengths, weaknesses, and fundamental score"
    )


def create_sentiment_analysis_task(agent: Agent, stock_symbol: str, company_name: str) -> Task:
    """Creates task for sentiment analysis"""
    return Task(
        description=f"""
        Perform comprehensive sentiment analysis for {stock_symbol} ({company_name}):
        1. Fetch and analyze global market news
        2. Fetch and analyze Indian market news
        3. Fetch and analyze company-specific news
        4. Calculate sentiment scores for each news category using NLP
        5. Determine overall market sentiment
        6. Assess how sentiment might impact stock price in the short term (1-4 weeks)
        
        Provide sentiment breakdown by category and overall sentiment score.
        """,
        agent=agent,
        expected_output="A detailed sentiment analysis report with sentiment scores for global news, Indian market news, company news, and overall sentiment assessment"
    )


def create_prediction_task(agent: Agent, stock_symbol: str, time_horizon_weeks: int, 
                          technical_analysis, fundamental_analysis, sentiment_analysis) -> Task:
    """Creates task for final prediction"""
    return Task(
        description=f"""
        Generate swing trading recommendation for {stock_symbol} with {time_horizon_weeks} week time horizon:
        
        1. Synthesize all analyses:
           - Technical analysis signals and indicators
           - Fundamental analysis strength and metrics
           - Sentiment analysis scores
        
        2. Generate recommendation (BUY, SELL, or HOLD) with:
           - Confidence score (0-100%)
           - Reasoning based on all three analyses
           - Target price range for the time horizon
           - Stop-loss suggestion
           - Risk level (LOW, MEDIUM, HIGH)
           - Position sizing suggestion
        
        3. Ensure recommendation is balanced and considers:
           - Technical signals strength
           - Fundamental health
           - Market sentiment
           - Time horizon for swing trading
        
        Provide a clear, actionable recommendation suitable for swing trading.
        """,
        agent=agent,
        expected_output="A comprehensive trading recommendation with action (BUY/SELL/HOLD), confidence score, target price, stop-loss, risk level, and detailed reasoning"
    )


def create_supervision_task(agent: Agent, stock_symbol: str, all_analyses: dict) -> Task:
    """Creates task for supervision and validation"""
    return Task(
        description=f"""
        Supervise and validate the complete analysis for {stock_symbol}:
        
        1. Validate data quality:
           - Check if all required data was collected
           - Verify data completeness and accuracy
           - Ensure real-time data was used
        
        2. Check analysis consistency:
           - Verify technical analysis is consistent with price data
           - Verify fundamental analysis uses correct metrics
           - Verify sentiment analysis covers all news sources
        
        3. Validate final recommendation:
           - Ensure recommendation is supported by evidence
           - Check if confidence score is justified
           - Verify target price and stop-loss are reasonable
           - Ensure risk assessment is appropriate
        
        4. Identify any errors or inconsistencies
        
        5. Provide final approval or flag issues
        
        Return a validation report with approval status and any concerns.
        """,
        agent=agent,
        expected_output="A validation report confirming data quality, analysis consistency, recommendation validity, and overall approval status"
    )

