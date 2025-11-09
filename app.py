"""
NSE Stock Trading Agent System - Streamlit UI
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.crew_config import StockAnalysisCrew

# Page configuration
st.set_page_config(
    page_title="NSE Stock Trading Agent",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .buy-signal {
        color: #00cc00;
        font-weight: bold;
    }
    .sell-signal {
        color: #ff3333;
        font-weight: bold;
    }
    .hold-signal {
        color: #ffaa00;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'stock_symbol' not in st.session_state:
    st.session_state.stock_symbol = None


def format_currency(value):
    """Format value as Indian currency"""
    if value is None:
        return "N/A"
    try:
        return f"₹{float(value):,.2f}"
    except (ValueError, TypeError):
        return "N/A"


def format_percentage(value):
    """Format value as percentage"""
    if value is None:
        return "N/A"
    try:
        return f"{float(value):.2f}%"
    except (ValueError, TypeError):
        return "N/A"


def create_candlestick_chart(historical_data, indicators=None):
    """Create candlestick chart with technical indicators"""
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=('Price Chart', 'Volume'),
        row_heights=[0.7, 0.3]
    )
    
    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=historical_data.index,
            open=historical_data['Open'],
            high=historical_data['High'],
            low=historical_data['Low'],
            close=historical_data['Close'],
            name='Price'
        ),
        row=1, col=1
    )
    
    # Add moving averages if available
    if indicators:
        if indicators.get('sma_20'):
            try:
                sma_20 = historical_data['Close'].rolling(window=20).mean()
                fig.add_trace(
                    go.Scatter(x=historical_data.index, y=sma_20, name='SMA 20', line=dict(color='blue')),
                    row=1, col=1
                )
            except:
                pass
        if indicators.get('sma_50') and len(historical_data) >= 50:
            try:
                sma_50 = historical_data['Close'].rolling(window=50).mean()
                fig.add_trace(
                    go.Scatter(x=historical_data.index, y=sma_50, name='SMA 50', line=dict(color='orange')),
                    row=1, col=1
                )
            except:
                pass
    
    # Volume chart
    if 'Volume' in historical_data.columns:
        colors = ['red' if historical_data['Close'].iloc[i] < historical_data['Open'].iloc[i] else 'green'
                 for i in range(len(historical_data))]
        fig.add_trace(
            go.Bar(x=historical_data.index, y=historical_data['Volume'], name='Volume', marker_color=colors),
            row=2, col=1
        )
    
    fig.update_layout(
        height=600,
        xaxis_rangeslider_visible=False,
        showlegend=True
    )
    
    return fig


def display_recommendation_card(recommendation):
    """Display the trading recommendation card"""
    action = recommendation.get('action', 'HOLD')
    confidence = recommendation.get('confidence', 0)
    target_price = recommendation.get('target_price', 0)
    stop_loss = recommendation.get('stop_loss', 0)
    risk_level = recommendation.get('risk_level', 'MEDIUM')
    reasoning = recommendation.get('reasoning', '')
    
    # Color based on action
    if action == 'BUY':
        color = '#00cc00'
        emoji = '🟢'
    elif action == 'SELL':
        color = '#ff3333'
        emoji = '🔴'
    else:
        color = '#ffaa00'
        emoji = '🟡'
    
    st.markdown(f"""
    <div style='background-color: #f0f2f6; padding: 2rem; border-radius: 1rem; border-left: 6px solid {color}; margin: 1rem 0;'>
        <h2 style='color: {color}; margin-bottom: 1rem;'>{emoji} Recommendation: {action}</h2>
        <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;'>
            <div>
                <strong>Confidence:</strong> <span style='font-size: 1.5rem; color: {color};'>{confidence}%</span>
            </div>
            <div>
                <strong>Risk Level:</strong> <span style='font-size: 1.2rem;'>{risk_level}</span>
            </div>
            <div>
                <strong>Target Price:</strong> {format_currency(target_price)}
            </div>
            <div>
                <strong>Stop Loss:</strong> {format_currency(stop_loss)}
            </div>
        </div>
        <div style='margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #ddd;'>
            <strong>Reasoning:</strong> {reasoning}
        </div>
    </div>
    """, unsafe_allow_html=True)


def main():
    # Header
    st.markdown('<div class="main-header">📈 NSE Stock Trading Agent System</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("📊 Stock Analysis Input")
        
        stock_symbol = st.text_input(
            "NSE Stock Symbol",
            value="RELIANCE",
            help="Enter NSE stock symbol (e.g., RELIANCE, TCS, INFY). Add .NS suffix if needed."
        )
        
        time_horizon = st.slider(
            "Time Horizon (Weeks)",
            min_value=1,
            max_value=4,
            value=2,
            help="Swing trading time horizon in weeks"
        )
        
        newsapi_key = st.text_input(
            "NewsAPI Key (Optional)",
            type="password",
            help="Get free API key from newsapi.org for better news coverage"
        )
        
        analyze_button = st.button("🔍 Analyze Stock", type="primary", use_container_width=True)
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        This system uses AI agents to analyze NSE stocks for swing trading:
        - **Technical Analysis**: 15+ indicators
        - **Fundamental Analysis**: 10+ metrics
        - **Sentiment Analysis**: Global & Indian news
        - **AI-Powered Prediction**: Combined recommendation
        """)
    
    # Main content area
    if analyze_button or st.session_state.analysis_results:
        if analyze_button:
            with st.spinner("🔄 Analyzing stock... This may take a minute."):
                try:
                    # Initialize crew
                    crew = StockAnalysisCrew(newsapi_key=newsapi_key if newsapi_key else None)
                    
                    # Perform analysis
                    results = crew.analyze_stock(stock_symbol, time_horizon_weeks=time_horizon)
                    
                    if 'error' in results:
                        st.error(f"❌ Error: {results['error']}")
                        st.session_state.analysis_results = None
                    else:
                        st.session_state.analysis_results = results
                        st.session_state.stock_symbol = stock_symbol
                        st.success("✅ Analysis complete!")
                except Exception as e:
                    st.error(f"❌ Error during analysis: {str(e)}")
                    import traceback
                    with st.expander("🔍 Error Details"):
                        st.code(traceback.format_exc())
                    st.session_state.analysis_results = None
        
        # Display results if available
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            
            # Stock Info
            st.markdown("## 📋 Stock Information")
            col1, col2, col3, col4 = st.columns(4)
            
            stock_info = results.get('stock_info', {})
            current_price = results.get('current_price', 0)
            
            with col1:
                st.metric("Company", stock_info.get('name', 'N/A'))
            with col2:
                st.metric("Current Price", format_currency(current_price))
            with col3:
                st.metric("Sector", stock_info.get('sector', 'N/A'))
            with col4:
                st.metric("Market Cap", format_currency(stock_info.get('market_cap', 0)))
            
            st.markdown("---")
            
            # Recommendation Card
            st.markdown("## 🎯 Trading Recommendation")
            recommendation = results.get('recommendation', {})
            display_recommendation_card(recommendation)
            
            # Tabs for detailed analysis
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Technical Analysis", "💰 Fundamental Analysis", "📰 Sentiment Analysis", "📈 Charts"])
            
            with tab1:
                st.markdown("### Technical Indicators")
                technical = results.get('technical_analysis', {})
                indicators = technical.get('indicators', {})
                signals = technical.get('signals', {})
                
                # Check if indicators are empty
                if not indicators or len(indicators) == 0:
                    st.warning("⚠️ Technical indicators are not available.")
                    st.info("""
                    **Possible reasons:**
                    - Insufficient historical data (need at least 20 trading days)
                    - Technical analysis library (`ta`) not installed
                    - Data fetching error
                    
                    **Solution:** 
                    - Install missing packages: `pip install ta`
                    - Try again later or check if the stock symbol is correct
                    """)

                else:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("#### Moving Averages")
                        sma_20 = indicators.get('sma_20')
                        sma_50 = indicators.get('sma_50')
                        sma_200 = indicators.get('sma_200')
                        ema_12 = indicators.get('ema_12')
                        ema_26 = indicators.get('ema_26')
                        
                        st.write(f"SMA 20: {format_currency(sma_20) if sma_20 else 'N/A'}")
                        st.write(f"SMA 50: {format_currency(sma_50) if sma_50 else 'N/A'}")
                        st.write(f"SMA 200: {format_currency(sma_200) if sma_200 else 'N/A'}")
                        st.write(f"EMA 12: {format_currency(ema_12) if ema_12 else 'N/A'}")
                        st.write(f"EMA 26: {format_currency(ema_26) if ema_26 else 'N/A'}")
                    
                    with col2:
                        st.markdown("#### Momentum Indicators")
                        rsi = indicators.get('rsi')
                        macd = indicators.get('macd')
                        macd_signal = indicators.get('macd_signal')
                        stoch_k = indicators.get('stoch_k')
                        stoch_d = indicators.get('stoch_d')
                        williams_r = indicators.get('williams_r')
                        cci = indicators.get('cci')
                        roc = indicators.get('roc')
                        
                        st.write(f"RSI: {rsi:.2f}" if rsi is not None else "RSI: N/A")
                        st.write(f"MACD: {macd:.4f}" if macd is not None else "MACD: N/A")
                        st.write(f"MACD Signal: {macd_signal:.4f}" if macd_signal is not None else "MACD Signal: N/A")
                        st.write(f"Stochastic %K: {stoch_k:.2f}" if stoch_k is not None else "Stochastic %K: N/A")
                        st.write(f"Stochastic %D: {stoch_d:.2f}" if stoch_d is not None else "Stochastic %D: N/A")
                        st.write(f"Williams %R: {williams_r:.2f}" if williams_r is not None else "Williams %R: N/A")
                        st.write(f"CCI: {cci:.2f}" if cci is not None else "CCI: N/A")
                        st.write(f"ROC: {format_percentage(roc)}" if roc is not None else "ROC: N/A")
                    
                    with col3:
                        st.markdown("#### Volatility & Volume")
                        atr = indicators.get('atr')
                        bb_upper = indicators.get('bb_upper')
                        bb_lower = indicators.get('bb_lower')
                        volume_ratio = indicators.get('volume_ratio')
                        adx = indicators.get('adx')
                        trend = indicators.get('trend', 'N/A')
                        
                        st.write(f"ATR: {format_currency(atr) if atr else 'N/A'}")
                        st.write(f"BB Upper: {format_currency(bb_upper) if bb_upper else 'N/A'}")
                        st.write(f"BB Lower: {format_currency(bb_lower) if bb_lower else 'N/A'}")
                        st.write(f"Volume Ratio: {volume_ratio:.2f}x" if volume_ratio else "Volume Ratio: N/A")
                        st.write(f"ADX: {adx:.2f}" if adx is not None else "ADX: N/A")
                        st.write(f"Trend: {trend}")
                    
                    st.markdown("#### Trading Signals")
                    signal_strength = signals.get('signal_strength', 0)
                    buy_signals = signals.get('buy_signals', 0)
                    sell_signals = signals.get('sell_signals', 0)
                    
                    st.write(f"**Signal Strength:** {signal_strength:.2f}")
                    st.write(f"Buy Signals: {buy_signals}")
                    st.write(f"Sell Signals: {sell_signals}")
                    
                    if signals.get('reasoning'):
                        st.write("**Reasoning:**")
                        for reason in signals['reasoning']:
                            st.write(f"- {reason}")
                    else:
                        st.info("No trading signals generated yet.")
            
            with tab2:
                st.markdown("### Fundamental Metrics")
                fundamental = results.get('fundamental_analysis', {})
                
                st.metric("Overall Score", f"{fundamental.get('score', 0):.1f}/100")
                st.metric("Assessment", fundamental.get('overall_assessment', 'N/A'))
                
                metrics = fundamental.get('metrics', {})
                if metrics:
                    st.markdown("#### Financial Ratios")
                    df_metrics = pd.DataFrame([
                        {'Metric': k.replace('_', ' ').title(), 'Value': v.get('value', 'N/A'), 'Status': v.get('status', 'N/A')}
                        for k, v in metrics.items()
                    ])
                    st.dataframe(df_metrics, use_container_width=True)
                else:
                    st.warning("No fundamental metrics available")
                
                strengths = fundamental.get('strengths', [])
                weaknesses = fundamental.get('weaknesses', [])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### ✅ Strengths")
                    if strengths:
                        for strength in strengths:
                            st.write(f"- {strength}")
                    else:
                        st.info("No strengths identified")
                
                with col2:
                    st.markdown("#### ⚠️ Weaknesses")
                    if weaknesses:
                        for weakness in weaknesses:
                            st.write(f"- {weakness}")
                    else:
                        st.info("No weaknesses identified")
            
            with tab3:
                st.markdown("### Sentiment Analysis")
                sentiment = results.get('sentiment_analysis', {})
                news_summary = results.get('news_summary', {})
                
                total_news = (news_summary.get('global_news_count', 0) + 
                              news_summary.get('indian_news_count', 0) + 
                              news_summary.get('company_news_count', 0))
                
                if total_news == 0:
                    st.warning("⚠️ No news articles were fetched.")
                    st.info("""
                    **Possible reasons:**
                    - RSS feeds are temporarily unavailable
                    - No NewsAPI key provided (optional but recommended)
                    - Network connectivity issues
                    - Sentiment analysis libraries not installed
                    
                    **Solution:** 
                    - Add a NewsAPI key in the sidebar for better news coverage
                    - Install missing packages: `pip install vaderSentiment textblob`
                    - Try again later
                    - News sentiment will be neutral without articles
                    """)
                else:
                    overall_sentiment = sentiment.get('overall_sentiment', 0)
                    sentiment_label = sentiment.get('overall_sentiment_label', 'NEUTRAL')
                    
                    st.metric("Overall Sentiment", sentiment_label)
                    st.metric("Sentiment Score", f"{overall_sentiment * 100:.2f}")
                    
                    # Sentiment breakdown
                    col1, col2, col3 = st.columns(3)
                    
                    global_news = sentiment.get('global_news', {})
                    indian_news = sentiment.get('indian_market_news', {})
                    company_news = sentiment.get('company_news', {})
                    
                    with col1:
                        st.markdown("#### Global News")
                        if global_news and global_news.get('count', 0) > 0:
                            avg_sent = global_news.get('average_sentiment', 0)
                            count = global_news.get('count', 0)
                            label = global_news.get('sentiment_label', 'N/A')
                            st.write(f"Average: {avg_sent * 100:.2f}")
                            st.write(f"Count: {count}")
                            st.write(f"Label: {label}")
                        else:
                            st.write("No global news available")
                    
                    with col2:
                        st.markdown("#### Indian Market News")
                        if indian_news and indian_news.get('count', 0) > 0:
                            avg_sent = indian_news.get('average_sentiment', 0)
                            count = indian_news.get('count', 0)
                            label = indian_news.get('sentiment_label', 'N/A')
                            st.write(f"Average: {avg_sent * 100:.2f}")
                            st.write(f"Count: {count}")
                            st.write(f"Label: {label}")
                        else:
                            st.write("No Indian market news available")
                    
                    with col3:
                        st.markdown("#### Company News")
                        if company_news and company_news.get('count', 0) > 0:
                            avg_sent = company_news.get('average_sentiment', 0)
                            count = company_news.get('count', 0)
                            label = company_news.get('sentiment_label', 'N/A')
                            st.write(f"Average: {avg_sent * 100:.2f}")
                            st.write(f"Count: {count}")
                            st.write(f"Label: {label}")
                        else:
                            st.write("No company news available")
                    
                    # Show news summary
                    if news_summary:
                        st.markdown("#### News Summary")
                        st.write(f"Total Global News: {news_summary.get('global_news_count', 0)}")
                        st.write(f"Total Indian News: {news_summary.get('indian_news_count', 0)}")
                        st.write(f"Total Company News: {news_summary.get('company_news_count', 0)}")
            
            with tab4:
                st.markdown("### Price Charts")
                try:
                    from data.stock_fetcher import StockFetcher
                    fetcher = StockFetcher()
                    historical_data = fetcher.get_historical_data(stock_symbol, period="6mo")
                    
                    if not historical_data.empty:
                        indicators = results.get('technical_analysis', {}).get('indicators', {})
                        fig = create_candlestick_chart(historical_data, indicators)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("Historical data not available for charting")
                except Exception as e:
                    st.error(f"Error creating chart: {str(e)}")
    
    else:
        # Welcome screen
        st.markdown("""
        ## Welcome to NSE Stock Trading Agent System! 🚀
        
        This AI-powered system analyzes Indian stocks (NSE) for swing trading using:
        
        - **🤖 Multi-Agent AI System**: Specialized agents for different analysis types
        - **📊 Technical Analysis**: 15+ technical indicators (RSI, MACD, Bollinger Bands, etc.)
        - **💰 Fundamental Analysis**: 10+ financial metrics (P/E, ROE, Debt-to-Equity, etc.)
        - **📰 Sentiment Analysis**: Real-time news from global, Indian market, and company sources
        - **🎯 Smart Predictions**: Combined AI recommendation with confidence scores
        
        ### How to Use:
        1. Enter an NSE stock symbol in the sidebar (e.g., RELIANCE, TCS, INFY)
        2. Select your swing trading time horizon (1-4 weeks)
        3. (Optional) Add your NewsAPI key for better news coverage
        4. Click "Analyze Stock" to get comprehensive analysis
        
        ### Example Stocks:
        - RELIANCE (Reliance Industries)
        - TCS (Tata Consultancy Services)
        - INFY (Infosys)
        - HDFCBANK (HDFC Bank)
        - ICICIBANK (ICICI Bank)
        
        **Note**: All data is fetched in real-time from public sources.
        """)
        
        # Example analysis
        st.markdown("---")
        st.markdown("### Quick Start")
        example_stocks = ["RELIANCE", "TCS", "INFY", "HDFCBANK"]
        cols = st.columns(len(example_stocks))
        for i, stock in enumerate(example_stocks):
            with cols[i]:
                if st.button(f"Analyze {stock}", key=f"example_{stock}"):
                    st.session_state.stock_symbol = stock
                    st.rerun()


if __name__ == "__main__":
    main()