# RustChain Miner Docker Image

Production-ready Docker image for RustChain miner.

## Features

- Multi-stage build (~50MB final image)
- Non-root user for security
- Production ready configuration
- Docker Compose support

## Usage

```bash
docker build -t rustchain-miner .
docker run -d --name rustchain-miner -e WALLET_ADDRESS=YOUR_WALLET rustchain-miner
```

## Files

- Dockerfile - Multi-stage build
- docker-compose.yml - Docker Compose config
- README.md - Documentation

---

Fixes #1599
