#!/usr/bin/env python3
"""
RustChain MCP Tool - Model Context Protocol integration
Allows Claude Code to interact with RustChain blockchain
"""

from mcp.server.fastmcp import FastMCP
import requests

# Initialize MCP server
mcp = FastMCP("RustChain")

# Configuration
RPC_URL = "https://rpc.rustchain.com"


@mcp.tool()
def get_balance(address: str) -> dict:
    """
    Get RTC balance for an address.
    
    Args:
        address: RTC wallet address
        
    Returns:
        Balance in wei and RTC
    """
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address, "latest"],
        "id": 1
    }
    
    try:
        response = requests.post(RPC_URL, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json().get("result", "0x0")
        balance_wei = int(result, 16) if result != "0x0" else 0
        balance_rtc = balance_wei / 1e18
        return {
            "address": address,
            "balance_wei": balance_wei,
            "balance_rtc": balance_rtc
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_block_info(block_number: int = None) -> dict:
    """
    Get block information.
    
    Args:
        block_number: Block number (optional, defaults to latest)
        
    Returns:
        Block information
    """
    if block_number is None:
        # Get latest block first
        payload = {"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1}
        response = requests.post(RPC_URL, json=payload, timeout=10)
        block_number = int(response.json().get("result", "0x0"), 16)
    
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBlockByNumber",
        "params": [hex(block_number), False],
        "id": 1
    }
    
    try:
        response = requests.post(RPC_URL, json=payload, timeout=10)
        response.raise_for_status()
        return response.json().get("result", {})
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_transaction(tx_hash: str) -> dict:
    """
    Get transaction details.
    
    Args:
        tx_hash: Transaction hash
        
    Returns:
        Transaction information
    """
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getTransactionByHash",
        "params": [tx_hash],
        "id": 1
    }
    
    try:
        response = requests.post(RPC_URL, json=payload, timeout=10)
        response.raise_for_status()
        return response.json().get("result", {})
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_network_stats() -> dict:
    """
    Get RustChain network statistics.
    
    Returns:
        Network stats including chain ID, latest block, gas price
    """
    stats = {}
    
    # Get chain ID
    payload = {"jsonrpc": "2.0", "method": "eth_chainId", "params": [], "id": 1}
    response = requests.post(RPC_URL, json=payload, timeout=10)
    stats["chain_id"] = int(response.json().get("result", "0x0"), 16)
    
    # Get latest block
    payload = {"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1}
    response = requests.post(RPC_URL, json=payload, timeout=10)
    stats["latest_block"] = int(response.json().get("result", "0x0"), 16)
    
    # Get gas price
    payload = {"jsonrpc": "2.0", "method": "eth_gasPrice", "params": [], "id": 1}
    response = requests.post(RPC_URL, json=payload, timeout=10)
    gas_price = int(response.json().get("result", "0x0"), 16)
    stats["gas_price_gwei"] = gas_price / 1e9
    
    return stats


if __name__ == "__main__":
    mcp.run()
