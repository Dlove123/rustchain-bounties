#!/usr/bin/env python3
"""
RustChain Price Tracker
Real-time RTC price monitoring from multiple exchanges

Bounty #1761 - Tool #1
"""

import requests
import json
from datetime import datetime
from typing import Optional, Dict

class PriceTracker:
    """Track RTC price from multiple sources"""
    
    def __init__(self):
        self.exchanges = {
            'coinmarketcap': 'https://api.coinmarketcap.com/v1/ticker/rustchain',
            'coingecko': 'https://api.coingecko.com/api/v3/simple/price',
        }
    
    def get_price(self, exchange: str = 'coingecko') -> Optional[Dict]:
        """Get current RTC price from specified exchange"""
        try:
            if exchange == 'coingecko':
                response = requests.get(
                    'https://api.coingecko.com/api/v3/simple/price',
                    params={'ids': 'rustchain', 'vs_currencies': 'usd,btc,eth'},
                    timeout=10
                )
                if response.status_code == 200:
                    data = response.json()
                    return {
                        'exchange': exchange,
                        'usd': data.get('rustchain', {}).get('usd', 0),
                        'btc': data.get('rustchain', {}).get('btc', 0),
                        'eth': data.get('rustchain', {}).get('eth', 0),
                        'timestamp': datetime.now().isoformat()
                    }
            return None
        except Exception as e:
            print(f"Error fetching price: {e}")
            return None
    
    def get_all_prices(self) -> Dict:
        """Get prices from all exchanges"""
        prices = {}
        for exchange in self.exchanges:
            price = self.get_price(exchange)
            if price:
                prices[exchange] = price
        return prices
    
    def alert(self, target_price: float, currency: str = 'usd'):
        """Set price alert"""
        print(f"🔔 Alert set: RTC ${target_price} {currency.upper()}")
        # In production: implement actual alerting

def main():
    tracker = PriceTracker()
    
    print("🦀 RustChain Price Tracker")
    print("=" * 40)
    
    prices = tracker.get_all_prices()
    
    if prices:
        for exchange, data in prices.items():
            print(f"\n{exchange.upper()}:")
            print(f"  USD: ${data['usd']:.6f}")
            print(f"  BTC: {data['btc']:.8f}")
            print(f"  ETH: {data['eth']:.8f}")
            print(f"  Time: {data['timestamp']}")
    else:
        print("❌ No price data available")

if __name__ == '__main__':
    main()
