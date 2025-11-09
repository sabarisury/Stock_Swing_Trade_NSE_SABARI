"""
Fundamental Analysis Module for stock financial metrics
"""
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FundamentalAnalyzer:
    """Analyzes fundamental/financial metrics of a stock"""
    
    def __init__(self):
        pass
    
    def analyze_fundamentals(self, fundamental_data: Dict) -> Dict:
        """Analyze fundamental metrics and generate score"""
        analysis = {
            'score': 0.0,
            'max_score': 100.0,
            'metrics': {},
            'strengths': [],
            'weaknesses': [],
            'overall_assessment': 'NEUTRAL'
        }
        
        try:
            pe_ratio = fundamental_data.get('pe_ratio')
            pb_ratio = fundamental_data.get('pb_ratio')
            debt_to_equity = fundamental_data.get('debt_to_equity')
            roe = fundamental_data.get('roe')
            roa = fundamental_data.get('roa')
            profit_margin = fundamental_data.get('profit_margin')
            revenue_growth = fundamental_data.get('revenue_growth')
            earnings_growth = fundamental_data.get('earnings_growth')
            current_ratio = fundamental_data.get('current_ratio')
            beta = fundamental_data.get('beta')
            
            score = 0.0
            max_possible = 0.0
            
            # P/E Ratio Analysis (15 points)
            if pe_ratio is not None:
                max_possible += 15
                if 10 <= pe_ratio <= 25:
                    score += 15
                    analysis['strengths'].append("Reasonable P/E ratio")
                elif pe_ratio < 10:
                    score += 10
                    analysis['strengths'].append("Low P/E ratio (potentially undervalued)")
                elif 25 < pe_ratio <= 35:
                    score += 8
                    analysis['weaknesses'].append("High P/E ratio")
                else:
                    score += 3
                    analysis['weaknesses'].append("Very high P/E ratio")
                analysis['metrics']['pe_ratio'] = {'value': pe_ratio, 'status': 'GOOD' if 10 <= pe_ratio <= 25 else 'CAUTION'}
            
            # P/B Ratio Analysis (10 points)
            if pb_ratio is not None:
                max_possible += 10
                if 1 <= pb_ratio <= 3:
                    score += 10
                    analysis['strengths'].append("Reasonable P/B ratio")
                elif pb_ratio < 1:
                    score += 8
                    analysis['strengths'].append("Low P/B ratio (potentially undervalued)")
                elif 3 < pb_ratio <= 5:
                    score += 5
                    analysis['weaknesses'].append("High P/B ratio")
                else:
                    score += 2
                    analysis['weaknesses'].append("Very high P/B ratio")
                analysis['metrics']['pb_ratio'] = {'value': pb_ratio, 'status': 'GOOD' if 1 <= pb_ratio <= 3 else 'CAUTION'}
            
            # Debt-to-Equity Analysis (15 points)
            if debt_to_equity is not None:
                max_possible += 15
                if debt_to_equity < 1:
                    score += 15
                    analysis['strengths'].append("Low debt-to-equity ratio (strong financial position)")
                elif 1 <= debt_to_equity < 2:
                    score += 12
                    analysis['strengths'].append("Moderate debt-to-equity ratio")
                elif 2 <= debt_to_equity < 3:
                    score += 7
                    analysis['weaknesses'].append("High debt-to-equity ratio")
                else:
                    score += 2
                    analysis['weaknesses'].append("Very high debt-to-equity ratio (high risk)")
                analysis['metrics']['debt_to_equity'] = {'value': debt_to_equity, 'status': 'GOOD' if debt_to_equity < 2 else 'CAUTION'}
            
            # ROE Analysis (15 points)
            if roe is not None:
                max_possible += 15
                roe_pct = roe * 100
                if roe_pct > 15:
                    score += 15
                    analysis['strengths'].append(f"Strong ROE ({roe_pct:.2f}%)")
                elif roe_pct > 10:
                    score += 12
                    analysis['strengths'].append(f"Good ROE ({roe_pct:.2f}%)")
                elif roe_pct > 5:
                    score += 8
                    analysis['weaknesses'].append(f"Moderate ROE ({roe_pct:.2f}%)")
                else:
                    score += 3
                    analysis['weaknesses'].append(f"Low ROE ({roe_pct:.2f}%)")
                analysis['metrics']['roe'] = {'value': roe_pct, 'status': 'GOOD' if roe_pct > 10 else 'CAUTION'}
            
            # ROA Analysis (10 points)
            if roa is not None:
                max_possible += 10
                roa_pct = roa * 100
                if roa_pct > 5:
                    score += 10
                    analysis['strengths'].append(f"Strong ROA ({roa_pct:.2f}%)")
                elif roa_pct > 3:
                    score += 8
                    analysis['strengths'].append(f"Good ROA ({roa_pct:.2f}%)")
                else:
                    score += 4
                    analysis['weaknesses'].append(f"Low ROA ({roa_pct:.2f}%)")
                analysis['metrics']['roa'] = {'value': roa_pct, 'status': 'GOOD' if roe_pct > 3 else 'CAUTION'}
            
            # Profit Margin Analysis (10 points)
            if profit_margin is not None:
                max_possible += 10
                margin_pct = profit_margin * 100
                if margin_pct > 15:
                    score += 10
                    analysis['strengths'].append(f"High profit margin ({margin_pct:.2f}%)")
                elif margin_pct > 10:
                    score += 8
                    analysis['strengths'].append(f"Good profit margin ({margin_pct:.2f}%)")
                elif margin_pct > 5:
                    score += 5
                    analysis['weaknesses'].append(f"Moderate profit margin ({margin_pct:.2f}%)")
                else:
                    score += 2
                    analysis['weaknesses'].append(f"Low profit margin ({margin_pct:.2f}%)")
                analysis['metrics']['profit_margin'] = {'value': margin_pct, 'status': 'GOOD' if margin_pct > 10 else 'CAUTION'}
            
            # Revenue Growth Analysis (10 points)
            if revenue_growth is not None:
                max_possible += 10
                growth_pct = revenue_growth * 100
                if growth_pct > 15:
                    score += 10
                    analysis['strengths'].append(f"Strong revenue growth ({growth_pct:.2f}%)")
                elif growth_pct > 10:
                    score += 8
                    analysis['strengths'].append(f"Good revenue growth ({growth_pct:.2f}%)")
                elif growth_pct > 5:
                    score += 5
                    analysis['weaknesses'].append(f"Moderate revenue growth ({growth_pct:.2f}%)")
                else:
                    score += 2
                    analysis['weaknesses'].append(f"Low/negative revenue growth ({growth_pct:.2f}%)")
                analysis['metrics']['revenue_growth'] = {'value': growth_pct, 'status': 'GOOD' if growth_pct > 10 else 'CAUTION'}
            
            # Earnings Growth Analysis (10 points)
            if earnings_growth is not None:
                max_possible += 10
                growth_pct = earnings_growth * 100
                if growth_pct > 20:
                    score += 10
                    analysis['strengths'].append(f"Strong earnings growth ({growth_pct:.2f}%)")
                elif growth_pct > 10:
                    score += 8
                    analysis['strengths'].append(f"Good earnings growth ({growth_pct:.2f}%)")
                elif growth_pct > 5:
                    score += 5
                    analysis['weaknesses'].append(f"Moderate earnings growth ({growth_pct:.2f}%)")
                else:
                    score += 2
                    analysis['weaknesses'].append(f"Low/negative earnings growth ({growth_pct:.2f}%)")
                analysis['metrics']['earnings_growth'] = {'value': growth_pct, 'status': 'GOOD' if growth_pct > 10 else 'CAUTION'}
            
            # Current Ratio Analysis (5 points)
            if current_ratio is not None:
                max_possible += 5
                if current_ratio > 2:
                    score += 5
                    analysis['strengths'].append("Strong liquidity (high current ratio)")
                elif current_ratio > 1:
                    score += 4
                    analysis['strengths'].append("Adequate liquidity")
                else:
                    score += 1
                    analysis['weaknesses'].append("Low current ratio (liquidity concerns)")
                analysis['metrics']['current_ratio'] = {'value': current_ratio, 'status': 'GOOD' if current_ratio > 1 else 'CAUTION'}
            
            # Quick Ratio Analysis (5 points)
            quick_ratio = fundamental_data.get('quick_ratio')
            if quick_ratio is not None:
                max_possible += 5
                if quick_ratio > 1.5:
                    score += 5
                    analysis['strengths'].append("Strong quick ratio (good short-term liquidity)")
                elif quick_ratio > 1:
                    score += 4
                    analysis['strengths'].append("Adequate quick ratio")
                else:
                    score += 2
                    analysis['weaknesses'].append("Low quick ratio")
                analysis['metrics']['quick_ratio'] = {'value': quick_ratio, 'status': 'GOOD' if quick_ratio > 1 else 'CAUTION'}
            
            # PEG Ratio Analysis (5 points)
            peg_ratio = fundamental_data.get('peg_ratio')
            if peg_ratio is not None:
                max_possible += 5
                if 0 < peg_ratio < 1:
                    score += 5
                    analysis['strengths'].append("Low PEG ratio (potentially undervalued)")
                elif 1 <= peg_ratio <= 2:
                    score += 4
                    analysis['strengths'].append("Reasonable PEG ratio")
                elif peg_ratio > 2:
                    score += 2
                    analysis['weaknesses'].append("High PEG ratio")
                else:
                    score += 1
                analysis['metrics']['peg_ratio'] = {'value': peg_ratio, 'status': 'GOOD' if 0 < peg_ratio < 2 else 'CAUTION'}
            
            # Operating Margin Analysis (5 points)
            operating_margin = fundamental_data.get('operating_margin')
            if operating_margin is not None:
                max_possible += 5
                margin_pct = operating_margin * 100
                if margin_pct > 20:
                    score += 5
                    analysis['strengths'].append(f"High operating margin ({margin_pct:.2f}%)")
                elif margin_pct > 15:
                    score += 4
                    analysis['strengths'].append(f"Good operating margin ({margin_pct:.2f}%)")
                elif margin_pct > 10:
                    score += 3
                    analysis['weaknesses'].append(f"Moderate operating margin ({margin_pct:.2f}%)")
                else:
                    score += 1
                    analysis['weaknesses'].append(f"Low operating margin ({margin_pct:.2f}%)")
                analysis['metrics']['operating_margin'] = {'value': margin_pct, 'status': 'GOOD' if margin_pct > 15 else 'CAUTION'}
            
            # Dividend Yield Analysis (5 points)
            dividend_yield = fundamental_data.get('dividend_yield')
            if dividend_yield is not None:
                max_possible += 5
                yield_pct = dividend_yield * 100 if dividend_yield < 1 else dividend_yield
                if yield_pct > 3:
                    score += 5
                    analysis['strengths'].append(f"Good dividend yield ({yield_pct:.2f}%)")
                elif yield_pct > 1.5:
                    score += 4
                    analysis['strengths'].append(f"Moderate dividend yield ({yield_pct:.2f}%)")
                elif yield_pct > 0:
                    score += 2
                    analysis['weaknesses'].append(f"Low dividend yield ({yield_pct:.2f}%)")
                else:
                    score += 0
                analysis['metrics']['dividend_yield'] = {'value': yield_pct, 'status': 'GOOD' if yield_pct > 1.5 else 'CAUTION'}
            
            # Beta Analysis (5 points)
            if beta is not None:
                max_possible += 5
                if 0.8 <= beta <= 1.2:
                    score += 5
                    analysis['strengths'].append("Moderate volatility (beta close to market)")
                elif beta < 0.8:
                    score += 4
                    analysis['strengths'].append("Low volatility (defensive stock)")
                elif beta > 1.5:
                    score += 2
                    analysis['weaknesses'].append("High volatility (aggressive stock)")
                else:
                    score += 3
                analysis['metrics']['beta'] = {'value': beta, 'status': 'GOOD' if 0.8 <= beta <= 1.2 else 'CAUTION'}
            
            # Calculate final score
            if max_possible > 0:
                analysis['score'] = (score / max_possible) * 100
            else:
                analysis['score'] = 50.0  # Default neutral score
            
            # Overall assessment
            if analysis['score'] >= 70:
                analysis['overall_assessment'] = 'STRONG'
            elif analysis['score'] >= 50:
                analysis['overall_assessment'] = 'MODERATE'
            else:
                analysis['overall_assessment'] = 'WEAK'
            
        except Exception as e:
            logger.error(f"Error analyzing fundamentals: {str(e)}")
            analysis['overall_assessment'] = 'ERROR'
        
        return analysis

