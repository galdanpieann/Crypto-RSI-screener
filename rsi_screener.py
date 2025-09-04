#!/usr/bin/env python3
"""
Crypto RSI Screener

Fetches cryptocurrency data and calculates RSI (Relative Strength Index)
to identify potentially oversold/overbought conditions.
"""

import json
import requests
from datetime import datetime
import os


def calculate_rsi(prices, period=14):
    """Calculate RSI for a series of prices using pure Python."""
    if len(prices) < period + 1:
        return [50.0] * len(prices)  # Return neutral RSI if not enough data
    
    # Calculate price changes
    deltas = []
    for i in range(1, len(prices)):
        deltas.append(prices[i] - prices[i-1])
    
    # Calculate initial average gain and loss
    initial_gains = [delta for delta in deltas[:period] if delta > 0]
    initial_losses = [-delta for delta in deltas[:period] if delta < 0]
    
    avg_gain = sum(initial_gains) / period if initial_gains else 0
    avg_loss = sum(initial_losses) / period if initial_losses else 0
    
    rsi_values = [50.0] * period  # Initialize with neutral values
    
    # Calculate RSI for remaining periods
    for i in range(period, len(deltas)):
        delta = deltas[i]
        
        if delta > 0:
            gain = delta
            loss = 0
        else:
            gain = 0
            loss = -delta
        
        # Update averages using Wilder's smoothing
        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period
        
        # Calculate RSI
        if avg_loss == 0:
            rsi = 100.0
        else:
            rs = avg_gain / avg_loss
            rsi = 100.0 - (100.0 / (1.0 + rs))
        
        rsi_values.append(rsi)
    
    # Ensure we have the same length as input prices
    while len(rsi_values) < len(prices):
        rsi_values.append(rsi_values[-1])
    
    return rsi_values


def fetch_crypto_data():
    """Fetch top cryptocurrencies data from CoinGecko API."""
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 50,
        'page': 1,
        'sparkline': True,
        'price_change_percentage': '24h,7d'
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []


def analyze_crypto_rsi():
    """Analyze cryptocurrency RSI and categorize coins."""
    print("Fetching cryptocurrency data...")
    crypto_data = fetch_crypto_data()
    
    if not crypto_data:
        print("No data available")
        return None
    
    results = []
    
    for coin in crypto_data:
        try:
            # Get sparkline data (7 days of price data)
            sparkline = coin.get('sparkline_in_7d', {}).get('price', [])
            
            if len(sparkline) < 14:  # Need at least 14 data points for RSI
                continue
                
            # Filter out None values
            prices = [float(p) for p in sparkline if p is not None]
            
            if len(prices) < 14:
                continue
                
            # Calculate RSI
            rsi_values = calculate_rsi(prices)
            current_rsi = rsi_values[-1]
            
            # Categorize based on RSI
            if current_rsi <= 30:
                category = "Oversold"
            elif current_rsi >= 70:
                category = "Overbought"
            else:
                category = "Neutral"
            
            results.append({
                'symbol': coin['symbol'].upper(),
                'name': coin['name'],
                'current_price': coin['current_price'],
                'market_cap': coin['market_cap'],
                'market_cap_rank': coin['market_cap_rank'],
                'price_change_24h': coin.get('price_change_percentage_24h', 0),
                'price_change_7d': coin.get('price_change_percentage_7d_in_currency', 0),
                'rsi': round(current_rsi, 2),
                'category': category
            })
            
        except Exception as e:
            print(f"Error processing {coin.get('name', 'Unknown')}: {e}")
            continue
    
    # Sort by RSI value
    results.sort(key=lambda x: x['rsi'])
    
    return results


def generate_html_report(results, output_dir='docs'):
    """Generate HTML report for GitHub Pages."""
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crypto RSI Screener</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .oversold {{ color: #28a745; }}
        .overbought {{ color: #dc3545; }}
        .neutral {{ color: #6c757d; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #f8f9fa;
            font-weight: 600;
        }}
        tr:hover {{
            background-color: #f8f9fa;
        }}
        .rsi-cell {{
            font-weight: bold;
        }}
        .category-badge {{
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: bold;
            color: white;
        }}
        .badge-oversold {{ background-color: #28a745; }}
        .badge-overbought {{ background-color: #dc3545; }}
        .badge-neutral {{ background-color: #6c757d; }}
        .updated {{
            text-align: center;
            margin-top: 20px;
            color: #6c757d;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 Crypto RSI Screener</h1>
        <p>Relative Strength Index analysis for top 50 cryptocurrencies by market cap</p>
    </div>
"""

    if results:
        # Calculate statistics
        oversold = len([r for r in results if r['category'] == 'Oversold'])
        overbought = len([r for r in results if r['category'] == 'Overbought'])
        neutral = len([r for r in results if r['category'] == 'Neutral'])
        
        html_content += f"""
    <div class="stats">
        <div class="stat-card">
            <div class="stat-number oversold">{oversold}</div>
            <div>Oversold (RSI ≤ 30)</div>
        </div>
        <div class="stat-card">
            <div class="stat-number neutral">{neutral}</div>
            <div>Neutral (30 < RSI < 70)</div>
        </div>
        <div class="stat-card">
            <div class="stat-number overbought">{overbought}</div>
            <div>Overbought (RSI ≥ 70)</div>
        </div>
    </div>

    <table>
        <thead>
            <tr>
                <th>Rank</th>
                <th>Symbol</th>
                <th>Name</th>
                <th>Price (USD)</th>
                <th>24h Change</th>
                <th>7d Change</th>
                <th>RSI</th>
                <th>Category</th>
            </tr>
        </thead>
        <tbody>
"""
        
        for coin in results:
            rsi_class = coin['category'].lower()
            badge_class = f"badge-{coin['category'].lower()}"
            
            price_24h = coin['price_change_24h']
            price_7d = coin['price_change_7d']
            
            price_24h_color = 'color: #28a745;' if price_24h > 0 else 'color: #dc3545;' if price_24h < 0 else ''
            price_7d_color = 'color: #28a745;' if price_7d > 0 else 'color: #dc3545;' if price_7d < 0 else ''
            
            html_content += f"""
            <tr>
                <td>#{coin['market_cap_rank']}</td>
                <td><strong>{coin['symbol']}</strong></td>
                <td>{coin['name']}</td>
                <td>${coin['current_price']:,.4f}</td>
                <td style="{price_24h_color}">{price_24h:+.2f}%</td>
                <td style="{price_7d_color}">{price_7d:+.2f}%</td>
                <td class="rsi-cell {rsi_class}">{coin['rsi']}</td>
                <td><span class="category-badge {badge_class}">{coin['category']}</span></td>
            </tr>
"""
        
        html_content += """
        </tbody>
    </table>
"""
    else:
        html_content += """
    <div style="text-align: center; padding: 40px; background: white; border-radius: 8px;">
        <h3>No data available</h3>
        <p>Unable to fetch cryptocurrency data at this time.</p>
    </div>
"""
    
    html_content += f"""
    <div class="updated">
        <p>Last updated: {timestamp}</p>
        <p>Data source: <a href="https://www.coingecko.com/" target="_blank">CoinGecko API</a></p>
    </div>
</body>
</html>
"""
    
    # Write HTML file
    with open(os.path.join(output_dir, 'index.html'), 'w') as f:
        f.write(html_content)
    
    # Write JSON data
    with open(os.path.join(output_dir, 'data.json'), 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'results': results,
            'stats': {
                'oversold': oversold if results else 0,
                'neutral': neutral if results else 0,
                'overbought': overbought if results else 0,
                'total': len(results)
            }
        }, f, indent=2)
    
    print(f"Generated report in {output_dir}/ directory")
    return os.path.join(output_dir, 'index.html')


def main():
    """Main function to run the RSI screener."""
    print("🚀 Crypto RSI Screener Starting...")
    
    results = analyze_crypto_rsi()
    
    if results:
        print(f"Analyzed {len(results)} cryptocurrencies")
        
        # Display summary
        oversold = len([r for r in results if r['category'] == 'Oversold'])
        overbought = len([r for r in results if r['category'] == 'Overbought'])
        neutral = len([r for r in results if r['category'] == 'Neutral'])
        
        print(f"\nSummary:")
        print(f"  Oversold (RSI ≤ 30): {oversold}")
        print(f"  Neutral (30 < RSI < 70): {neutral}")
        print(f"  Overbought (RSI ≥ 70): {overbought}")
        
        # Show top oversold and overbought
        if oversold > 0:
            print(f"\nMost Oversold:")
            for coin in results[:3]:
                if coin['category'] == 'Oversold':
                    print(f"  {coin['symbol']}: RSI {coin['rsi']}")
        
        if overbought > 0:
            print(f"\nMost Overbought:")
            overbought_coins = [c for c in results if c['category'] == 'Overbought']
            overbought_coins.sort(key=lambda x: x['rsi'], reverse=True)
            for coin in overbought_coins[:3]:
                print(f"  {coin['symbol']}: RSI {coin['rsi']}")
        
        # Generate HTML report
        output_file = generate_html_report(results)
        print(f"\nHTML report generated: {output_file}")
        
    else:
        print("No results to display")
        # Still generate empty report
        generate_html_report([])


if __name__ == "__main__":
    main()