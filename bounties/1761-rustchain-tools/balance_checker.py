#!/usr/bin/env python3
"""
RustChain Wallet Balance Checker
Check multiple wallet balances in bulk

Bounty #1761 - Tool #3
"""

import requests
from typing import List, Dict

class BalanceChecker:
    """Check wallet balances in bulk"""
    
    def __init__(self, rpc_url: str = "https://50.28.86.131"):
        self.rpc_url = rpc_url
    
    def check_balance(self, address: str) -> Dict:
        """Check balance for single address"""
        try:
            url = f"{self.rpc_url}/wallet/balance?miner_id={address}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'address': address,
                    'balance': data.get('balance', 0),
                    'confirmed': data.get('confirmed', 0),
                    'success': True
                }
            return {
                'address': address,
                'balance': 0,
                'error': f"HTTP {response.status_code}",
                'success': False
            }
        except Exception as e:
            return {
                'address': address,
                'balance': 0,
                'error': str(e),
                'success': False
            }
    
    def check_bulk(self, addresses: List[str]) -> List[Dict]:
        """Check balances for multiple addresses"""
        results = []
        for addr in addresses:
            result = self.check_balance(addr)
            results.append(result)
            print(f"✅ {addr}: {result['balance']} RTC")
        return results
    
    def export_csv(self, results: List[Dict], filename: str = "balances.csv"):
        """Export results to CSV"""
        with open(filename, 'w') as f:
            f.write("Address,Balance,Confirmed,Status\n")
            for r in results:
                status = "OK" if r['success'] else f"Error: {r.get('error', 'Unknown')}"
                f.write(f"{r['address']},{r['balance']},{r.get('confirmed', 0)},{status}\n")
        print(f"📊 Exported to {filename}")

def main():
    checker = BalanceChecker()
    
    print("💰 RustChain Balance Checker")
    print("=" * 50)
    
    # Example addresses (replace with real ones)
    addresses = [
        "RTC1234567890abcdef",
        "RTCabcdef1234567890",
    ]
    
    results = checker.check_bulk(addresses)
    
    total = sum(r['balance'] for r in results if r['success'])
    print(f"\nTotal Balance: {total} RTC")
    
    # Export
    checker.export_csv(results)

if __name__ == '__main__':
    main()
