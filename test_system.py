"""
Test script for the NSE Stock Trading Agent System
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.crew_config import StockAnalysisCrew

def test_stock_analysis():
    """Test the stock analysis system with a sample stock"""
    print("=" * 60)
    print("Testing NSE Stock Trading Agent System")
    print("=" * 60)
    
    # Test with RELIANCE
    test_symbol = "RELIANCE"
    time_horizon = 2
    
    print(f"\n📊 Analyzing {test_symbol}...")
    print(f"⏱️  Time Horizon: {time_horizon} weeks\n")
    
    try:
        # Initialize crew
        crew = StockAnalysisCrew(newsapi_key=None)  # Using free sources only
        
        # Perform analysis
        results = crew.analyze_stock(test_symbol, time_horizon_weeks=time_horizon)
        
        if 'error' in results:
            print(f"❌ Error: {results['error']}")
            return False
        
        # Display results
        print("\n" + "=" * 60)
        print("ANALYSIS RESULTS")
        print("=" * 60)
        
        # Stock Info
        stock_info = results.get('stock_info', {})
        print(f"\n📋 Stock Information:")
        print(f"   Company: {stock_info.get('name', 'N/A')}")
        print(f"   Sector: {stock_info.get('sector', 'N/A')}")
        print(f"   Current Price: ₹{results.get('current_price', 0):,.2f}")
        
        # Recommendation
        recommendation = results.get('recommendation', {})
        print(f"\n🎯 Recommendation:")
        print(f"   Action: {recommendation.get('action', 'N/A')}")
        print(f"   Confidence: {recommendation.get('confidence', 0):.1f}%")
        print(f"   Target Price: ₹{recommendation.get('target_price', 0):,.2f}")
        print(f"   Stop Loss: ₹{recommendation.get('stop_loss', 0):,.2f}")
        print(f"   Risk Level: {recommendation.get('risk_level', 'N/A')}")
        print(f"   Reasoning: {recommendation.get('reasoning', 'N/A')}")
        
        # Technical Analysis Summary
        technical = results.get('technical_analysis', {})
        indicators = technical.get('indicators', {})
        signals = technical.get('signals', {})
        print(f"\n📊 Technical Analysis:")
        print(f"   RSI: {indicators.get('rsi', 0):.2f}")
        print(f"   Trend: {indicators.get('trend', 'N/A')}")
        print(f"   Signal Strength: {signals.get('signal_strength', 0):.2f}")
        
        # Fundamental Analysis Summary
        fundamental = results.get('fundamental_analysis', {})
        print(f"\n💰 Fundamental Analysis:")
        print(f"   Score: {fundamental.get('score', 0):.1f}/100")
        print(f"   Assessment: {fundamental.get('overall_assessment', 'N/A')}")
        
        # Sentiment Analysis Summary
        sentiment = results.get('sentiment_analysis', {})
        print(f"\n📰 Sentiment Analysis:")
        print(f"   Overall Sentiment: {sentiment.get('overall_sentiment_label', 'N/A')}")
        print(f"   Sentiment Score: {sentiment.get('overall_sentiment', 0) * 100:.2f}")
        
        print("\n" + "=" * 60)
        print("✅ Test completed successfully!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_stock_analysis()
    sys.exit(0 if success else 1)

