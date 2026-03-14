# RustChain Miner Docker Image

Production-ready Docker image for RustChain miner.

## Features

- **Multi-stage build** - Minimal image size (~50MB)
- **Non-root user** - Security best practice
- **Production ready** - Proper logging and restart policy
- **Easy deployment** - Docker Compose included

## Quick Start

### Build

```bash
docker build -t rustchain-miner .
```

### Run

```bash
docker run -d \
  --name rustchain-miner \
  -e WALLET_ADDRESS=YOUR_WALLET \
  -e RPC_URL=https://rpc.rustchain.com \
  -v miner-data:/app/data \
  --restart unless-stopped \
  rustchain-miner
```

### Docker Compose

```bash
# Edit docker-compose.yml with your wallet address
# Then run:
docker-compose up -d
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `WALLET_ADDRESS` | Your RTC wallet | Required |
| `RPC_URL` | RustChain RPC endpoint | https://rpc.rustchain.com |

## Files

- `Dockerfile` - Multi-stage Docker build
- `docker-compose.yml` - Docker Compose configuration
- `README.md` - This documentation

---

Fixes #1599
