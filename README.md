# Crypto RSI Screener

A daily cryptocurrency RSI (Relative Strength Index) screener that analyzes the top 50 cryptocurrencies by market cap and publishes results to GitHub Pages.

## 🎯 What it does

The screener:
- Fetches real-time data for the top 50 cryptocurrencies by market cap from CoinGecko API
- Calculates RSI (Relative Strength Index) using 14-period lookback on 7-day price data
- Categorizes coins as **Oversold** (RSI ≤ 30), **Neutral** (30 < RSI < 70), or **Overbought** (RSI ≥ 70)
- Generates an interactive HTML report with statistics and detailed coin analysis
- Automatically deploys results to GitHub Pages for easy viewing

## 🔄 Automated Workflow

The analysis runs automatically:
- **Daily at 12:00 UTC** via scheduled workflow
- **On every push to main branch** for testing
- **Manual trigger available** for on-demand analysis

## 🚀 Running Manually

### Via GitHub Actions (Recommended)
1. Go to the **Actions** tab in this repository
2. Select **"Daily RSI Screener"** workflow
3. Click **"Run workflow"** button
4. Optionally enable debug output
5. Click **"Run workflow"** to start

### Local Development
```bash
# Clone the repository
git clone https://github.com/galdanpieann/crypto-rsi-screener.git
cd crypto-rsi-screener

# Install dependencies
pip install -r requirements.txt

# Run the screener
python rsi_screener.py
```

The script will:
1. Fetch cryptocurrency data from CoinGecko
2. Calculate RSI for each coin
3. Generate HTML report in `docs/` directory
4. Display summary statistics in terminal

## 📊 Viewing Results

### GitHub Pages (Live Results)
The latest analysis results are automatically published to:
**https://galdanpieann.github.io/crypto-rsi-screener/**

The page includes:
- Summary statistics (count of oversold/neutral/overbought coins)
- Sortable table with all analyzed cryptocurrencies
- Real-time price data and RSI values
- Color-coded categories for easy identification

### JSON Data
Raw data is also available at:
**https://galdanpieann.github.io/crypto-rsi-screener/data.json**

## 🔧 Technical Details

### RSI Calculation
- Uses 14-period RSI calculation on 7-day price history
- Oversold threshold: RSI ≤ 30 (potential buying opportunity)
- Overbought threshold: RSI ≥ 70 (potential selling signal)

### Data Source
- **CoinGecko API**: Free tier, no authentication required
- **Rate limits**: Respects API rate limits with error handling
- **Fallback**: Generates empty report if API is unavailable

### GitHub Pages Deployment
- Uses official GitHub Actions: `actions/upload-pages-artifact` + `actions/deploy-pages`
- Deployed to `github-pages` environment
- Automatic deployment on successful analysis
- Static HTML/CSS/JSON files only

## 📁 Repository Structure

```
├── .github/workflows/
│   └── rsi-screener.yml    # Main workflow file
├── docs/                   # Generated GitHub Pages content
│   ├── index.html         # Main report page
│   └── data.json          # Raw analysis data
├── rsi_screener.py        # Main analysis script
├── requirements.txt       # Python dependencies
├── .gitignore            # Standard Python/Node ignores
└── README.md             # This file
```

## 🛠️ Workflow Configuration

The workflow is configured with:
- **Environment**: `github-pages` 
- **Permissions**: `contents: read`, `pages: write`, `id-token: write`
- **Concurrency**: Single deployment, non-canceling
- **Python version**: 3.11 with pip caching
- **Triggers**: Schedule, manual dispatch, push to main

## 📈 Understanding RSI

RSI (Relative Strength Index) is a momentum oscillator that measures the speed and change of price movements:

- **0-30**: Oversold (potential buying opportunity)
- **30-70**: Neutral (normal trading range)  
- **70-100**: Overbought (potential selling signal)

*Note: RSI is just one indicator and should not be used as the sole basis for trading decisions.*

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally with `python rsi_screener.py`
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.