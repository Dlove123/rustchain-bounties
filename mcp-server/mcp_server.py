#!/usr/bin/env python3
"""
RustChain MCP Server - Query RustChain from Claude Code

Implements Model Context Protocol (MCP) for RustChain blockchain queries.
"""

import asyncio
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("RustChain")

# RustChain RPC endpoint
RUSTCHAIN_RPC = "https://50.28.86.131"

@mcp.tool()
async def get_health() -> dict:
    """Get RustChain node health status"""
    async with httpx.AsyncClient(verify=False) as client:
        resp = await client.get(f"{RUSTCHAIN_RPC}/health")
        return resp.json()

@mcp.tool()
async def get_epoch() -> dict:
    """Get current epoch information"""
    async with httpx.AsyncClient(verify=False) as client:
        resp = await client.get(f"{RUSTCHAIN_RPC}/epoch")
        return resp.json()

@mcp.tool()
async def get_miners() -> list:
    """Get list of active miners"""
    async with httpx.AsyncClient(verify=False) as client:
        resp = await client.get(f"{RUSTCHAIN_RPC}/api/miners")
        return resp.json()

@mcp.tool()
async def get_wallet_balance(miner_id: str) -> dict:
    """Get wallet balance for a miner ID"""
    async with httpx.AsyncClient(verify=False) as client:
        resp = await client.get(
            f"{RUSTCHAIN_RPC}/wallet/balance",
            params={"miner_id": miner_id}
        )
        return resp.json()

@mcp.tool()
async def get_block_info(block_number: int = None) -> dict:
    """Get block information (latest or specific block)"""
    async with httpx.AsyncClient(verify=False) as client:
        if block_number:
            resp = await client.get(f"{RUSTCHAIN_RPC}/block/{block_number}")
        else:
            resp = await client.get(f"{RUSTCHAIN_RPC}/block/latest")
        return resp.json()

if __name__ == "__main__":
    # Run MCP server
    mcp.run()
