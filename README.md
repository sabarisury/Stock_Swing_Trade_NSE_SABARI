# NSE Stock Trading Agent System

An AI-powered multi-agent system for analyzing Indian stock market (NSE) stocks for swing trading. The system uses CrewAI framework with specialized agents for technical analysis, fundamental analysis, and sentiment analysis.

## Features

- **🤖 Multi-Agent AI System**: Specialized CrewAI agents for different analysis types
- **📊 Technical Analysis**: 15+ technical indicators including:
  - Moving Averages (SMA 20, 50, 200; EMA 12, 26)
  - Momentum indicators (RSI, MACD, Stochastic, Williams %R, ROC, PPO)
  - Volatility indicators (Bollinger Bands, ATR)
  - Volume indicators (Volume ratio, OBV)
  - Trend indicators (ADX, CCI)
  - Support and Resistance levels

- **💰 Fundamental Analysis**: 10+ financial metrics including:
  - Valuation ratios (P/E, Forward P/E, P/B, PEG)
  - Profitability (ROE, ROA, Profit Margin, Operating Margin)
  - Growth metrics (Revenue Growth, Earnings Growth)
  - Financial health (Debt-to-Equity, Current Ratio, Quick Ratio)
  - Market metrics (Beta, Dividend Yield)

- **📰 Sentiment Analysis**: Real-time news analysis from:
  - Global market news
  - Indian market news (Economic Times, etc.)
  - Company-specific news
  - NLP-based sentiment scoring (VADER + TextBlob)

- **🎯 Smart Predictions**: Combined AI recommendation with:
  - Buy/Sell/Hold recommendation
  - Confidence score (0-100%)
  - Target price and stop-loss levels
  - Risk assessment
  - Position sizing suggestions

- **📈 Interactive UI**: Beautiful Streamlit interface with:
  - Real-time stock data
  - Interactive charts (candlestick with indicators)
  - Comprehensive analysis breakdown
  - Detailed recommendation cards

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd BigMart
```

2. Install dependencies:
```bash
pip install -r requirement.txt
```

3. (Optional) Get NewsAPI key:
   - Sign up at https://newsapi.org (free tier: 100 requests/day)
   - Add your API key in the Streamlit UI sidebar

## Usage

### Streamlit UI (Recommended)

Run the Streamlit application:
```bash
streamlit run app.py
```

Then:
1. Enter an NSE stock symbol (e.g., RELIANCE, TCS, INFY)
2. Select time horizon (1-4 weeks for swing trading)
3. (Optional) Add NewsAPI key for better news coverage
4. Click "Analyze Stock"

### Command Line Testing

Test the system with a sample stock:
```bash
python test_system.py
```

## Project Structure

```
BigMart/
├── agents/
│   ├── stock_agents.py      # CrewAI agent definitions
│   └── crew_config.py        # Crew configuration and orchestration
├── data/
│   ├── stock_fetcher.py      # yfinance wrapper for NSE stocks
│   └── news_fetcher.py       # News aggregation from multiple sources
├── analysis/
│   ├── technical_analyzer.py    # Technical indicators calculation
│   ├── fundamental_analyzer.py  # Fundamental metrics analysis
│   └── sentiment_analyzer.py    # News sentiment analysis
├── prediction/
│   └── trading_predictor.py     # Final recommendation generator
├── app.py                    # Streamlit UI
├── test_system.py           # Test script
└── requirement.txt          # Python dependencies
```

## How It Works

1. **Data Collection**: Fetches real-time stock data from yfinance (supports NSE with `.NS` suffix)
2. **Parallel Analysis**:
   - Technical Agent: Calculates 15+ technical indicators
   - Fundamental Agent: Analyzes 10+ financial metrics
   - Sentiment Agent: Fetches and analyzes news from multiple sources
3. **Prediction**: Combines all analyses with weighted scoring
4. **Supervision**: Validates data quality and analysis consistency
5. **Recommendation**: Generates actionable swing trading recommendation

## Data Sources

All data sources are **free/public**:
- **Stock Data**: yfinance (Yahoo Finance API)
- **News**: 
  - NewsAPI.org (free tier)
  - RSS feeds (Economic Times, etc.)
  - Web scraping (with rate limiting)

## Example Stocks

- RELIANCE (Reliance Industries)
- TCS (Tata Consultancy Services)
- INFY (Infosys)
- HDFCBANK (HDFC Bank)
- ICICIBANK (ICICI Bank)

## Deployment

### Streamlit Cloud (Recommended)
1. Push code to GitHub
2. Connect to Streamlit Cloud: https://streamlit.io/cloud
3. Deploy from repository

### Other Platforms
- **Railway**: Supports Python apps, easy Git deployment
- **Render**: Free tier for web services
- **Heroku**: Paid, reliable for Python apps

Note: Vercel is not ideal for Streamlit apps (designed for serverless/static sites).

## Requirements

- Python 3.8+
- All dependencies listed in `requirement.txt`

## License

This project is for educational and research purposes. Always do your own research before making investment decisions.

## Disclaimer

This system is for informational purposes only. Stock market investments carry risk. Always consult with a financial advisor before making investment decisions. The authors are not responsible for any financial losses.

