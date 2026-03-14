# RustChain Node Health Monitor CLI

Command-line tool for monitoring RustChain node health.

## Features

- **Node Health Check** - Verify node is online and responding
- **Peer Count** - Monitor connected peers
- **Sync Status** - Check if node is synced
- **Balance Query** - Check account balance
- **Block Details** - Get block information

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Check Node Health

```bash
python monitor.py
python monitor.py --rpc https://rpc.rustchain.com
```

### Check Balance

```bash
python monitor.py --balance RTC1234567890abcdef...
```

### Get Block Details

```bash
python monitor.py --block 1000000
```

### Output

```
🔍 Checking node health at https://rpc.rustchain.com...

✅ Node Status: ONLINE
📦 Latest Block: #1,234,567
🔗 Chain ID: 1234
⛽ Gas Price: 25.50 Gwei
👥 Peer Count: 8 ✅ Good
✅ Sync Status: SYNCED

⏰ Checked at: 2026-03-14 11:15:00
```

## Files

- `monitor.py` - Main CLI tool
- `requirements.txt` - Dependencies
- `README.md` - Documentation

---

Fixes #1606
