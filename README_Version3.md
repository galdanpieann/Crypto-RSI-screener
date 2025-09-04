# Crypto RSI(4) Screener — Binance USDT Perpetuals

Client-side screener for Binance USDⓈ-M Perpetual USDT pairs on the 1D timeframe:
- RSI period: 4 (using only the last 4 fully closed daily candles)
- Market cap filter via CoinGecko
- RSI cross detection for levels 30, 50, and 70 (up- and down-cross on the latest closed bar)

## GitHub Pages

This repo deploys the screener from `docs/` to GitHub Pages via GitHub Actions.

- Workflow: `.github/workflows/deploy-pages.yml`
- Entry point: `docs/index.html`
- Expected URL after the first successful run:
  https://galdanpieann.github.io/crypto-rsi-screener/

If you see a 404, wait for the first deployment to complete or check the Actions tab.

## Local use

Open `docs/index.html` in your browser. Everything runs client-side.

## Notes

- Binance data source: USDⓈ-M Futures API (1d klines). We exclude leveraged tokens and odd-multiplier symbols.
- CoinGecko is used for market caps and 24h change. Symbol-to-asset mapping is by base ticker; ambiguous tickers may be omitted.
- RSI crosses:
  - Up-cross: previous RSI below the level and current RSI at/above the level.
  - Down-cross: previous RSI above the level and current RSI at/below the level.