#!/usr/bin/env python3
"""
RustChain Node Health Monitor CLI
Monitor node health, peer count, and sync status
"""

import argparse
import json
import requests
import sys
from datetime import datetime

# Configuration
DEFAULT_RPC_URL = "https://rpc.rustchain.com"


def rpc_call(rpc_url, method, params=None):
    """Make JSON-RPC call"""
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params or [],
        "id": 1
    }
    try:
        response = requests.post(rpc_url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json().get("result")
    except Exception as e:
        return {"error": str(e)}


def check_node_health(rpc_url):
    """Check overall node health"""
    print(f"\n🔍 Checking node health at {rpc_url}...\n")
    
    # Get block number
    block_num = rpc_call(rpc_url, "eth_blockNumber")
    if not block_num or "error" in str(block_num):
        print("❌ Node is not responding!")
        return False
    
    block_int = int(block_num, 16)
    print(f"✅ Node Status: ONLINE")
    print(f"📦 Latest Block: #{block_int:,}")
    
    # Get chain ID
    chain_id = rpc_call(rpc_url, "eth_chainId")
    if chain_id:
        print(f"🔗 Chain ID: {int(chain_id, 16)}")
    
    # Get gas price
    gas_price = rpc_call(rpc_url, "eth_gasPrice")
    if gas_price:
        gas_gwei = int(gas_price, 16) / 1e9
        print(f"⛽ Gas Price: {gas_gwei:.2f} Gwei")
    
    # Get peer count (net_peerCount)
    peer_count = rpc_call(rpc_url, "net_peerCount")
    if peer_count:
        peers = int(peer_count, 16)
        status = "✅ Good" if peers >= 5 else "⚠️ Low"
        print(f"👥 Peer Count: {peers} {status}")
    
    # Get sync status
    syncing = rpc_call(rpc_url, "eth_syncing")
    if syncing and syncing != False:
        print(f"🔄 Sync Status: SYNCING")
        if "currentBlock" in syncing:
            current = int(syncing["currentBlock"], 16)
            highest = int(syncing["highestBlock"], 16)
            progress = (current / highest * 100) if highest > 0 else 0
            print(f"   Progress: {progress:.1f}% ({current:,}/{highest:,})")
    else:
        print(f"✅ Sync Status: SYNCED")
    
    print(f"\n⏰ Checked at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return True


def get_balance(rpc_url, address):
    """Get account balance"""
    result = rpc_call(rpc_url, "eth_getBalance", [address, "latest"])
    if result and "error" not in str(result):
        balance_rtc = int(result, 16) / 1e18
        print(f"💰 Balance: {balance_rtc:.4f} RTC")
        return balance_rtc
    else:
        print(f"❌ Error: {result}")
        return None


def get_block(rpc_url, block_num):
    """Get block details"""
    result = rpc_call(rpc_url, "eth_getBlockByNumber", [hex(block_num), False])
    if result and "error" not in str(result):
        print(f"\n📦 Block #{block_num:,}")
        print(f"   Hash: {result['hash']}")
        print(f"   Transactions: {len(result['transactions'])}")
        print(f"   Timestamp: {datetime.fromtimestamp(int(result['timestamp'], 16))}")
        return result
    else:
        print(f"❌ Block not found")
        return None


def main():
    parser = argparse.ArgumentParser(description="RustChain Node Health Monitor")
    parser.add_argument("--rpc", default=DEFAULT_RPC_URL, help="RPC URL")
    parser.add_argument("--balance", metavar="ADDRESS", help="Check balance for address")
    parser.add_argument("--block", type=int, metavar="NUM", help="Get block details")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    if args.balance:
        get_balance(args.rpc, args.balance)
    elif args.block:
        get_block(args.rpc, args.block)
    else:
        check_node_health(args.rpc)


if __name__ == "__main__":
    main()
