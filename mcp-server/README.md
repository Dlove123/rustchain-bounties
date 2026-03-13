# RustChain MCP Server

[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-brightgreen)](https://modelcontextprotocol.io)
[![RustChain](https://img.shields.io/badge/RustChain-MCP%20Server-blue)](https://github.com/Scottcjn/RustChain)

Query RustChain blockchain data directly from Claude Code using Model Context Protocol (MCP).

## Features

- 🔍 **Health Check** - Monitor node status
- 📊 **Epoch Info** - Get current epoch and slot
- 👥 **Miners List** - Query active miners
- 💰 **Wallet Balance** - Check RTC balance
- 🔗 **Block Info** - Query block details

## Installation

```bash
# Clone the repository
cd rustchain-bounties/mcp-server

# Install dependencies
pip install -r requirements.txt
```

## Usage with Claude Code

### Start MCP Server

```bash
python mcp_server.py
```

### Available Tools

Once connected, you can use these tools in Claude Code:

1. **get_health** - Get node health status
2. **get_epoch** - Get current epoch information
3. **get_miners** - Get list of active miners
4. **get_wallet_balance** - Get wallet balance for a miner ID
5. **get_block_info** - Get block information

### Example Queries

```
@RustChain MCP What's the current epoch and slot?
@RustChain MCP Check the balance of miner victus-x86-scott
@RustChain MCP How many miners are currently active?
@RustChain MCP Is the RustChain node healthy?
```

## API Reference

### get_health()

Returns node health status.

```json
{
  "ok": true,
  "db_rw": true,
  "uptime_s": 24000,
  "version": "2.2.1-rip200"
}
```

### get_epoch()

Returns current epoch information.

```json
{
  "epoch": 73,
  "slot": 10554,
  "blocks_per_epoch": 144,
  "enrolled_miners": 12
}
```

### get_miners()

Returns list of active miners.

```json
[
  {
    "miner": "victus-x86-scott",
    "hardware_type": "x86",
    "antiquity_multiplier": 1.5
  }
]
```

### get_wallet_balance(miner_id: str)

Returns wallet balance for a specific miner.

**Parameters:**
- `miner_id` (string, required): The miner ID to query

```json
{
  "amount_i64": 265420827,
  "amount_rtc": 265.420827,
  "miner_id": "victus-x86-scott"
}
```

### get_block_info(block_number: int = None)

Returns block information.

**Parameters:**
- `block_number` (int, optional): Block number (default: latest)

## Development

### Running Tests

```bash
pytest test_mcp_server.py -v
```

### Adding New Tools

To add a new tool, simply add a new decorated function:

```python
@mcp.tool()
async def my_new_tool(param: str) -> dict:
    """Tool description"""
    # Implementation
    return result
```

## License

MIT License - See LICENSE file for details.

## Support

For issues or questions, please open an issue on the RustChain bounties repository.
