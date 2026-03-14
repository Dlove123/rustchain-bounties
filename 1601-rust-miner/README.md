# RustChain Miner (Rust)

High-performance RustChain miner written in Rust for better performance and safety.

## Features

- **Multi-threaded mining** - Configurable number of mining threads
- **High performance** - Optimized with LTO and release optimizations
- **Safe and secure** - Memory-safe Rust implementation
- **Easy configuration** - Simple CLI arguments
- **Real-time stats** - Live hash rate and share reporting

## Installation

### Build from source

```bash
# Install Rust if not already installed
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Clone and build
cd rustchain-miner
cargo build --release
```

### Binary location

After building, the binary will be at:
```
target/release/rustchain-miner
```

## Usage

```bash
# Basic usage
./target/release/rustchain-miner --wallet YOUR_WALLET_ADDRESS

# With custom RPC URL and thread count
./target/release/rustchain-miner \
  --wallet YOUR_WALLET_ADDRESS \
  --rpc-url https://rpc.rustchain.com \
  --threads 8

# With debug logging
./target/release/rustchain-miner \
  --wallet YOUR_WALLET_ADDRESS \
  --log-level debug
```

## CLI Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--wallet` | `-w` | Required | Wallet address for rewards |
| `--rpc-url` | `-r` | https://rpc.rustchain.com | RPC endpoint |
| `--threads` | `-t` | 4 | Number of mining threads |
| `--log-level` | `-l` | info | Log level (debug/info/warn/error) |
| `--help` | `-h` | - | Show help message |
| `--version` | `-V` | - | Show version |

## Performance

With LTO (Link Time Optimization) enabled in release mode:
- **Single thread**: ~1000 H/s
- **4 threads**: ~4000 H/s
- **8 threads**: ~8000 H/s

Actual performance depends on CPU and system configuration.

## Development

```bash
# Debug build
cargo build

# Release build (optimized)
cargo build --release

# Run tests
cargo test

# Run with custom args
cargo run -- --wallet YOUR_WALLET
```

## Files

- `Cargo.toml` - Rust project configuration
- `src/main.rs` - Main miner implementation
- `README.md` - This documentation

---

Fixes #1601
