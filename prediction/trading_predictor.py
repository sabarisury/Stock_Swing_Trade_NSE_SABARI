"""
Trading Predictor - Combines all analyses for final recommendation
"""
import pandas as pd
import numpy as np
from typing import Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TradingPredictor:
    """Generates swing trading recommendations by combining all analyses"""
    
    def __init__(self):
        pass
    
    def generate_recommendation(self, stock_symbol: str, current_price: float, 
                                time_horizon_weeks: int, technical_analysis: Dict,
                                fundamental_analysis: Dict, sentiment_analysis: Dict,
                                historical_data: pd.DataFrame) -> Dict:
        """
        Generate final trading recommendation
        
        Args:
            stock_symbol: Stock symbol
            current_price: Current stock price
            time_horizon_weeks: Time horizon in weeks
            technical_analysis: Technical analysis results
            fundamental_analysis: Fundamental analysis results
            sentiment_analysis: Sentiment analysis results
            historical_data: Historical price data
        
        Returns:
            Dictionary with recommendation details
        """
        try:
            # Extract scores and signals
            technical_signals = technical_analysis.get('signals', {})
            technical_signal_strength = technical_signals.get('signal_strength', 0.0)  # -100 to +100
            
            fundamental_score = fundamental_analysis.get('score', 50.0)  # 0 to 100
            fundamental_assessment = fundamental_analysis.get('overall_assessment', 'NEUTRAL')
            
            sentiment_score = sentiment_analysis.get('overall_sentiment', 0.0)  # -1 to 1
            sentiment_normalized = sentiment_score * 100  # -100 to +100
            
            # Weighted scoring system
            # Technical: 40%, Fundamental: 35%, Sentiment: 25%
            weighted_score = (
                (technical_signal_strength * 0.40) +
                ((fundamental_score - 50) * 0.70 * 0.35) +  # Normalize fundamental to -50 to +50
                (sentiment_normalized * 0.25)
            )
            
            # Determine recommendation
            if weighted_score >= 30:
                action = 'BUY'
                confidence = min(95, 50 + abs(weighted_score) * 0.9)
            elif weighted_score <= -30:
                action = 'SELL'
                confidence = min(95, 50 + abs(weighted_score) * 0.9)
            else:
                action = 'HOLD'
                confidence = max(30, 50 - abs(weighted_score) * 0.5)
            
            # Calculate target price and stop-loss
            target_price, stop_loss = self._calculate_price_targets(
                current_price, weighted_score, time_horizon_weeks, historical_data
            )
            
            # Determine risk level
            risk_level = self._assess_risk(
                technical_analysis, fundamental_analysis, sentiment_analysis, historical_data
            )
            
            # Generate reasoning
            reasoning = self._generate_reasoning(
                action, technical_signals, fundamental_assessment, 
                sentiment_analysis, weighted_score
            )
            
            # Position sizing suggestion
            position_size = self._suggest_position_size(confidence, risk_level)
            
            recommendation = {
                'action': action,
                'confidence': round(confidence, 1),
                'target_price': round(target_price, 2),
                'stop_loss': round(stop_loss, 2),
                'risk_level': risk_level,
                'reasoning': reasoning,
                'position_size': position_size,
                'time_horizon_weeks': time_horizon_weeks,
                'weighted_score': round(weighted_score, 2),
                'score_breakdown': {
                    'technical_contribution': round(technical_signal_strength * 0.40, 2),
                    'fundamental_contribution': round((fundamental_score - 50) * 0.70 * 0.35, 2),
                    'sentiment_contribution': round(sentiment_normalized * 0.25, 2)
                }
            }
            
            return recommendation
            
        except Exception as e:
            logger.error(f"Error generating recommendation: {str(e)}")
            return {
                'action': 'HOLD',
                'confidence': 0,
                'error': str(e)
            }
    
    def _calculate_price_targets(self, current_price: float, weighted_score: float,
                                 time_horizon_weeks: int, historical_data: pd.DataFrame) -> tuple:
        """Calculate target price and stop-loss"""
        try:
            # Calculate volatility (ATR or standard deviation)
            if not historical_data.empty and len(historical_data) > 20:
                returns = historical_data['Close'].pct_change().dropna()
                volatility = returns.std() * np.sqrt(252)  # Annualized volatility
                
                # Price movement estimate based on score and volatility
                # Higher score = more bullish, higher target
                price_change_pct = (weighted_score / 100) * volatility * (time_horizon_weeks / 52) * 2
                
                target_price = current_price * (1 + price_change_pct)
                
                # Stop-loss: 2-3% below current for buys, 2-3% above for sells
                if weighted_score > 0:
                    stop_loss = current_price * 0.97  # 3% stop-loss for buys
                else:
                    stop_loss = current_price * 1.03  # 3% stop-loss for sells
            else:
                # Default targets if insufficient data
                if weighted_score > 0:
                    target_price = current_price * 1.05  # 5% target
                    stop_loss = current_price * 0.97  # 3% stop-loss
                elif weighted_score < 0:
                    target_price = current_price * 0.95  # 5% target
                    stop_loss = current_price * 1.03  # 3% stop-loss
                else:
                    target_price = current_price
                    stop_loss = current_price * 0.98
            
            return target_price, stop_loss
            
        except Exception as e:
            logger.error(f"Error calculating price targets: {str(e)}")
            return current_price * 1.05, current_price * 0.97
    
    def _assess_risk(self, technical_analysis: Dict, fundamental_analysis: Dict,
                    sentiment_analysis: Dict, historical_data: pd.DataFrame) -> str:
        """Assess overall risk level"""
        try:
            risk_factors = 0
            
            # Technical risk
            indicators = technical_analysis.get('indicators', {})
            if indicators.get('atr'):
                volatility = indicators.get('atr', 0) / indicators.get('current_price', 1)
                if volatility > 0.05:  # High volatility
                    risk_factors += 1
            
            # Fundamental risk
            fundamental_score = fundamental_analysis.get('score', 50)
            if fundamental_score < 40:
                risk_factors += 1
            
            # Sentiment risk
            sentiment = sentiment_analysis.get('overall_sentiment', 0)
            if abs(sentiment) > 0.5:  # Very strong sentiment (could reverse)
                risk_factors += 1
            
            # Volatility risk from historical data
            if not historical_data.empty:
                returns = historical_data['Close'].pct_change().dropna()
                if returns.std() > 0.03:  # High daily volatility
                    risk_factors += 1
            
            if risk_factors >= 3:
                return 'HIGH'
            elif risk_factors >= 2:
                return 'MEDIUM'
            else:
                return 'LOW'
                
        except Exception as e:
            logger.error(f"Error assessing risk: {str(e)}")
            return 'MEDIUM'
    
    def _generate_reasoning(self, action: str, technical_signals: Dict,
                           fundamental_assessment: str, sentiment_analysis: Dict,
                           weighted_score: float) -> str:
        """Generate human-readable reasoning"""
        reasoning_parts = []
        
        # Technical reasoning
        tech_reasoning = technical_signals.get('reasoning', [])
        if tech_reasoning:
            reasoning_parts.append(f"Technical: {', '.join(tech_reasoning[:3])}")
        
        # Fundamental reasoning
        reasoning_parts.append(f"Fundamental: {fundamental_assessment} assessment")
        
        # Sentiment reasoning
        sentiment_label = sentiment_analysis.get('overall_sentiment_label', 'NEUTRAL')
        reasoning_parts.append(f"Sentiment: {sentiment_label}")
        
        # Overall
        if weighted_score > 30:
            reasoning_parts.append("Strong bullish signals across all analyses")
        elif weighted_score < -30:
            reasoning_parts.append("Strong bearish signals across all analyses")
        else:
            reasoning_parts.append("Mixed signals, suggesting cautious approach")
        
        return ". ".join(reasoning_parts) + "."
    
    def _suggest_position_size(self, confidence: float, risk_level: str) -> str:
        """Suggest position sizing"""
        if risk_level == 'HIGH':
            if confidence > 70:
                return "Small position (1-2% of portfolio)"
            else:
                return "Very small position (<1% of portfolio)"
        elif risk_level == 'MEDIUM':
            if confidence > 70:
                return "Moderate position (2-3% of portfolio)"
            else:
                return "Small position (1-2% of portfolio)"
        else:  # LOW risk
            if confidence > 70:
                return "Normal position (3-5% of portfolio)"
            else:
                return "Moderate position (2-3% of portfolio)"

