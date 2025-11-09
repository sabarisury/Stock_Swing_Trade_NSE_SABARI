"""
Technical Analysis Module for stock price data
"""
import pandas as pd
import numpy as np
import ta  # pyright: ignore[reportMissingImports]
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TechnicalAnalyzer:
    """Performs technical analysis on stock price data"""
    
    def __init__(self):
        pass
    
    def calculate_indicators(self, df: pd.DataFrame) -> Dict:
        """Calculate all technical indicators"""
        if df.empty:
            logger.warning("DataFrame is empty for technical analysis")
            return {}
        
        if len(df) < 20:
            logger.warning(f"Insufficient data for technical analysis: {len(df)} rows (need at least 20)")
            return {}
        
        # Check required columns
        required_cols = ['Open', 'High', 'Low', 'Close']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            logger.error(f"Missing required columns: {missing_cols}")
            return {}
        
        try:
            indicators = {}
            
            # Price-based indicators
            try:
                indicators['sma_20'] = float(ta.trend.SMAIndicator(df['Close'], window=20).sma_indicator().iloc[-1])
            except Exception as e:
                logger.error(f"Error calculating SMA 20: {e}")
                indicators['sma_20'] = None
            
            try:
                indicators['sma_50'] = float(ta.trend.SMAIndicator(df['Close'], window=50).sma_indicator().iloc[-1]) if len(df) >= 50 else None
            except Exception as e:
                logger.error(f"Error calculating SMA 50: {e}")
                indicators['sma_50'] = None
            
            try:
                indicators['sma_200'] = float(ta.trend.SMAIndicator(df['Close'], window=200).sma_indicator().iloc[-1]) if len(df) >= 200 else None
            except Exception as e:
                logger.error(f"Error calculating SMA 200: {e}")
                indicators['sma_200'] = None
            
            try:
                indicators['ema_12'] = float(ta.trend.EMAIndicator(df['Close'], window=12).ema_indicator().iloc[-1])
            except Exception as e:
                logger.error(f"Error calculating EMA 12: {e}")
                indicators['ema_12'] = None
            
            try:
                indicators['ema_26'] = float(ta.trend.EMAIndicator(df['Close'], window=26).ema_indicator().iloc[-1]) if len(df) >= 26 else None
            except Exception as e:
                logger.error(f"Error calculating EMA 26: {e}")
                indicators['ema_26'] = None
            
            # Momentum indicators
            try:
                indicators['rsi'] = float(ta.momentum.RSIIndicator(df['Close'], window=14).rsi().iloc[-1])
            except Exception as e:
                logger.error(f"Error calculating RSI: {e}")
                indicators['rsi'] = None
            
            try:
                macd = ta.trend.MACD(df['Close'])
                indicators['macd'] = float(macd.macd().iloc[-1])
                indicators['macd_signal'] = float(macd.macd_signal().iloc[-1])
                indicators['macd_diff'] = float(macd.macd_diff().iloc[-1])
            except Exception as e:
                logger.error(f"Error calculating MACD: {e}")
                indicators['macd'] = None
                indicators['macd_signal'] = None
                indicators['macd_diff'] = None
            
            # Stochastic Oscillator (needs High, Low, Close)
            try:
                if 'High' in df.columns and 'Low' in df.columns:
                    stoch = ta.momentum.StochasticOscillator(df['High'], df['Low'], df['Close'], window=14, smooth_window=3)
                    indicators['stoch_k'] = float(stoch.stoch().iloc[-1])
                    indicators['stoch_d'] = float(stoch.stoch_signal().iloc[-1])
                else:
                    indicators['stoch_k'] = None
                    indicators['stoch_d'] = None
            except Exception as e:
                logger.error(f"Error calculating Stochastic: {e}")
                indicators['stoch_k'] = None
                indicators['stoch_d'] = None
            
            # Continue with other indicators...
            # (Add similar try-except for each indicator)
            
            # ... rest of the indicators with similar error handling
            
            return indicators
            
        except Exception as e:
            logger.error(f"Error calculating technical indicators: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return {}
    
    
    
    def _calculate_support(self, df: pd.DataFrame, window: int = 20) -> float:
        """Calculate support level (local minimum)"""
        try:
            recent_lows = df['Low'].tail(window)
            return float(recent_lows.min())
        except:
            return float(df['Low'].min())
    
    def _calculate_resistance(self, df: pd.DataFrame, window: int = 20) -> float:
        """Calculate resistance level (local maximum)"""
        try:
            recent_highs = df['High'].tail(window)
            return float(recent_highs.max())
        except:
            return float(df['High'].max())
    
    def _determine_trend(self, df: pd.DataFrame, indicators: Dict) -> str:
        """Determine overall trend"""
        try:
            current_price = df['Close'].iloc[-1]
            sma_20 = indicators.get('sma_20')
            sma_50 = indicators.get('sma_50')
            
            if sma_50 and sma_20:
                if current_price > sma_20 > sma_50:
                    return "UPTREND"
                elif current_price < sma_20 < sma_50:
                    return "DOWNTREND"
                else:
                    return "SIDEWAYS"
            elif sma_20:
                if current_price > sma_20:
                    return "UPTREND"
                else:
                    return "DOWNTREND"
            else:
                return "NEUTRAL"
        except:
            return "NEUTRAL"
    
    def _calculate_momentum(self, df: pd.DataFrame, period: int = 10) -> float:
        """Calculate price momentum"""
        try:
            if len(df) < period + 1:
                return 0.0
            current_price = df['Close'].iloc[-1]
            past_price = df['Close'].iloc[-(period + 1)]
            return ((current_price - past_price) / past_price) * 100
        except:
            return 0.0
    
    def generate_signals(self, indicators: Dict) -> Dict:
        """Generate trading signals based on technical indicators"""
        signals = {
            'buy_signals': 0,
            'sell_signals': 0,
            'neutral_signals': 0,
            'signal_strength': 0.0,
            'reasoning': []
        }
        
        try:
            rsi = indicators.get('rsi', 50)
            macd_diff = indicators.get('macd_diff', 0)
            trend = indicators.get('trend', 'NEUTRAL')
            price_vs_sma20 = indicators.get('price_vs_sma20', 0)
            volume_ratio = indicators.get('volume_ratio', 1.0)
            current_price = indicators.get('current_price', 0)
            bb_upper = indicators.get('bb_upper', 0)
            bb_lower = indicators.get('bb_lower', 0)
            
            # RSI signals
            if rsi < 30:
                signals['buy_signals'] += 1
                signals['reasoning'].append("RSI indicates oversold condition")
            elif rsi > 70:
                signals['sell_signals'] += 1
                signals['reasoning'].append("RSI indicates overbought condition")
            else:
                signals['neutral_signals'] += 1
            
            # MACD signals
            if macd_diff > 0:
                signals['buy_signals'] += 1
                signals['reasoning'].append("MACD shows bullish momentum")
            elif macd_diff < 0:
                signals['sell_signals'] += 1
                signals['reasoning'].append("MACD shows bearish momentum")
            
            # Trend signals
            if trend == "UPTREND":
                signals['buy_signals'] += 1
                signals['reasoning'].append("Price is in uptrend")
            elif trend == "DOWNTREND":
                signals['sell_signals'] += 1
                signals['reasoning'].append("Price is in downtrend")
            
            # Price vs SMA signals
            if price_vs_sma20 > 2:
                signals['buy_signals'] += 1
                signals['reasoning'].append("Price is above 20-day SMA")
            elif price_vs_sma20 < -2:
                signals['sell_signals'] += 1
                signals['reasoning'].append("Price is below 20-day SMA")
            
            # Volume confirmation
            if volume_ratio > 1.5:
                signals['reasoning'].append("High volume confirms price movement")
            
            # Bollinger Bands
            if current_price < bb_lower:
                signals['buy_signals'] += 1
                signals['reasoning'].append("Price near lower Bollinger Band (potential bounce)")
            elif current_price > bb_upper:
                signals['sell_signals'] += 1
                signals['reasoning'].append("Price near upper Bollinger Band (potential reversal)")
            
            # Calculate signal strength (-100 to +100)
            total_signals = signals['buy_signals'] + signals['sell_signals'] + signals['neutral_signals']
            if total_signals > 0:
                signals['signal_strength'] = ((signals['buy_signals'] - signals['sell_signals']) / total_signals) * 100
            
        except Exception as e:
            logger.error(f"Error generating signals: {str(e)}")
        
        return signals

