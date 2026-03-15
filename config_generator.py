#!/usr/bin/env python3
"""
Configuration Generator for Verification Bot
Generate .env and config files automatically
"""

import os
import json

def generate_env_template():
    """Generate .env template"""
    template = """# Verification Bot Configuration
GITHUB_TOKEN=your_github_token_here
RUSTCHAIN_RPC_URL=https://50.28.86.131
PAYPAL_EMAIL=979749654@qq.com
ETH_ADDRESS=0x31e323edC293B940695ff04aD1AFdb56d473351D
RTC_ADDRESS=RTCb72a1accd46b9ba9f22dbd4b5c6aad5a5831572b
"""
    with open('.env.example', 'w') as f:
        f.write(template)
    print("✅ Generated .env.example")

def generate_payment_config():
    """Generate payment configuration"""
    config = {
        'paypal': '979749654@qq.com',
        'eth': '0x31e323edC293B940695ff04aD1AFdb56d473351D',
        'rtc': 'RTCb72a1accd46b9ba9f22dbd4b5c6aad5a5831572b',
        'github': 'Dlove123',
        'payment_terms': {
            'days': 30,
            'reminder_days': [10, 20, 25],
            'rollback_day': 30
        }
    }
    with open('payment_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    print("✅ Generated payment_config.json")

if __name__ == '__main__':
    generate_env_template()
    generate_payment_config()
