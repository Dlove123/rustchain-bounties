#!/usr/bin/env python3
"""
RustChain Mining Profitability Calculator
Calculate ROI for RTC mining operations

Bounty #1761 - Tool #2
"""

from typing import Dict

class MiningCalculator:
    """Calculate mining profitability"""
    
    def __init__(self, rtc_price: float = 0.10):
        self.rtc_price = rtc_price  # USD
    
    def calculate_profit(
        self,
        hashrate: float,  # H/s
        power_consumption: float,  # Watts
        electricity_cost: float,  # $/kWh
        pool_fee: float = 0.02,  # 2%
        difficulty: float = 1000000
    ) -> Dict:
        """Calculate daily/monthly/yearly profit"""
        
        # Simplified mining formula (in production use actual network stats)
        blocks_per_day = 1440  # 1 block per minute
        reward_per_block = 50  # RTC
        
        # Your share of rewards
        daily_rtc = (hashrate / difficulty) * blocks_per_day * reward_per_block
        daily_rtc *= (1 - pool_fee)
        
        # Revenue in USD
        daily_revenue = daily_rtc * self.rtc_price
        
        # Power cost
        daily_power_cost = (power_consumption / 1000) * 24 * electricity_cost
        
        # Profit
        daily_profit = daily_revenue - daily_power_cost
        
        return {
            'daily_rtc': daily_rtc,
            'daily_revenue_usd': daily_revenue,
            'daily_power_cost_usd': daily_power_cost,
            'daily_profit_usd': daily_profit,
            'monthly_profit_usd': daily_profit * 30,
            'yearly_profit_usd': daily_profit * 365,
            'roi_days': self._calculate_roi(hashrate, power_consumption, daily_profit)
        }
    
    def _calculate_roi(self, hashrate: float, power: float, daily_profit: float) -> float:
        """Calculate days to ROI (assuming $1000 initial investment)"""
        initial_investment = 1000  # USD (hardware cost)
        if daily_profit <= 0:
            return float('inf')
        return initial_investment / daily_profit

def main():
    calc = MiningCalculator(rtc_price=0.10)
    
    print("⛏️  RustChain Mining Calculator")
    print("=" * 50)
    
    # Example calculation
    result = calc.calculate_profit(
        hashrate=1000000,  # 1 MH/s
        power_consumption=500,  # 500W
        electricity_cost=0.12,  # $0.12/kWh
        pool_fee=0.02
    )
    
    print(f"\nDaily RTC: {result['daily_rtc']:.2f}")
    print(f"Daily Revenue: ${result['daily_revenue_usd']:.2f}")
    print(f"Daily Power Cost: ${result['daily_power_cost_usd']:.2f}")
    print(f"Daily Profit: ${result['daily_profit_usd']:.2f}")
    print(f"Monthly Profit: ${result['monthly_profit_usd']:.2f}")
    print(f"Yearly Profit: ${result['yearly_profit_usd']:.2f}")
    print(f"ROI: {result['roi_days']:.0f} days")

if __name__ == '__main__':
    main()
