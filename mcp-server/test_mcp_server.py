#!/usr/bin/env python3
"""
Tests for RustChain MCP Server
"""

import pytest
from mcp_server import get_health, get_epoch, get_miners, get_wallet_balance

@pytest.mark.asyncio
async def test_get_health():
    """Test health endpoint"""
    result = await get_health()
    assert "ok" in result
    assert result["ok"] == True

@pytest.mark.asyncio
async def test_get_epoch():
    """Test epoch endpoint"""
    result = await get_epoch()
    assert "epoch" in result
    assert "slot" in result

@pytest.mark.asyncio
async def test_get_miners():
    """Test miners endpoint"""
    result = await get_miners()
    assert isinstance(result, list)
    assert len(result) > 0

@pytest.mark.asyncio
async def test_get_wallet_balance():
    """Test wallet balance endpoint"""
    # Use a known miner ID for testing
    result = await get_wallet_balance("victus-x86-scott")
    assert "amount_rtc" in result
    assert "miner_id" in result

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
