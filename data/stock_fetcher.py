"""
Stock Data Fetcher for NSE stocks using yfinance
"""
import yfinance as yf
import pandas as pd
from typing import Dict, Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StockFetcher:
    """Fetches real-time and historical stock data for NSE stocks"""
    
    def __init__(self):
        self.cache = {}
    
    def _format_symbol(self, symbol: str) -> str:
        """Format NSE symbol for yfinance"""
        symbol = symbol.upper().strip()
        if not symbol.endswith('.NS'):
            symbol = f"{symbol}.NS"
        return symbol
    
    def get_stock_info(self, symbol: str) -> Dict:
        """Get basic stock information"""
        try:
            formatted_symbol = self._format_symbol(symbol)
            ticker = yf.Ticker(formatted_symbol)
            info = ticker.info
            
            return {
                'symbol': symbol,
                'name': info.get('longName', info.get('shortName', 'N/A')),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 0),
                'currency': info.get('currency', 'INR'),
                'exchange': info.get('exchange', 'NSE'),
            }
        except Exception as e:
            logger.error(f"Error fetching stock info for {symbol}: {str(e)}")
            return {}
    
    def get_current_price(self, symbol: str) -> Optional[float]:
        """Get current/latest stock price"""
        try:
            formatted_symbol = self._format_symbol(symbol)
            ticker = yf.Ticker(formatted_symbol)
            data = ticker.history(period="1d", interval="1m")
            
            if not data.empty:
                return float(data['Close'].iloc[-1])
            else:
                # Fallback to regular history
                data = ticker.history(period="5d")
                if not data.empty:
                    return float(data['Close'].iloc[-1])
            return None
        except Exception as e:
            logger.error(f"Error fetching current price for {symbol}: {str(e)}")
            return None
    
    def get_historical_data(self, symbol: str, period: str = "1y") -> pd.DataFrame:
        """Get historical price data"""
        try:
            formatted_symbol = self._format_symbol(symbol)
            ticker = yf.Ticker(formatted_symbol)
            data = ticker.history(period=period)
            
            if data.empty:
                logger.warning(f"No data found for {symbol}")
                return pd.DataFrame()
            
            return data
        except Exception as e:
            logger.error(f"Error fetching historical data for {symbol}: {str(e)}")
            return pd.DataFrame()
    
    def get_fundamental_data(self, symbol: str) -> Dict:
        """Get fundamental/financial metrics"""
        try:
            formatted_symbol = self._format_symbol(symbol)
            ticker = yf.Ticker(formatted_symbol)
            info = ticker.info
            
            fundamental_data = {
                'pe_ratio': info.get('trailingPE', None),
                'forward_pe': info.get('forwardPE', None),
                'pb_ratio': info.get('priceToBook', None),
                'peg_ratio': info.get('pegRatio', None),
                'debt_to_equity': info.get('debtToEquity', None),
                'current_ratio': info.get('currentRatio', None),
                'quick_ratio': info.get('quickRatio', None),
                'roe': info.get('returnOnEquity', None),
                'roa': info.get('returnOnAssets', None),
                'profit_margin': info.get('profitMargins', None),
                'operating_margin': info.get('operatingMargins', None),
                'revenue_growth': info.get('revenueGrowth', None),
                'earnings_growth': info.get('earningsGrowth', None),
                'dividend_yield': info.get('dividendYield', None),
                'beta': info.get('beta', None),
                '52_week_high': info.get('fiftyTwoWeekHigh', None),
                '52_week_low': info.get('fiftyTwoWeekLow', None),
                'book_value': info.get('bookValue', None),
                'enterprise_value': info.get('enterpriseValue', None),
            }
            
            return fundamental_data
        except Exception as e:
            logger.error(f"Error fetching fundamental data for {symbol}: {str(e)}")
            return {}
    
    def get_all_data(self, symbol: str, period: str = "1y") -> Dict:
        """Get all stock data in one call"""
        return {
            'info': self.get_stock_info(symbol),
            'current_price': self.get_current_price(symbol),
            'historical_data': self.get_historical_data(symbol, period),
            'fundamental_data': self.get_fundamental_data(symbol),
        }

