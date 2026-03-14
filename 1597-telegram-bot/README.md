# RustChain Telegram Bot

Telegram bot for querying RustChain blockchain data.

## Features

- `/balance <address>` - Query RTC balance
- `/block` - Get latest block number
- `/tx <hash>` - Get transaction details
- `/stats` - Get network statistics
- `/help` - Help message

## Setup

1. Create a Telegram bot via @BotFather
2. Get your bot token
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set environment variable:
   ```bash
   export TELEGRAM_TOKEN="your-bot-token"
   export RUSTCHAIN_RPC_URL="https://rpc.rustchain.com"
   ```
5. Run the bot:
   ```bash
   python bot.py
   ```

## Usage

```
/balance RTC1234567890abcdef
/block
/tx 0xabc123...
/stats
/help
```

---

Fixes #1597
