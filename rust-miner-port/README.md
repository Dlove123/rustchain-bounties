# RustChain Miner Port (Rust)

**Bounty**: #1601
**Value**: 15 RTC (~$1.5)
**Status**: In Progress

---

## 🦀 Features

- ✅ CLI with clap
- ✅ Async runtime (tokio)
- ✅ HTTP client (reqwest)
- ✅ Epoch info display
- ✅ Balance display
- ⏳ Mining logic (TODO)

---

## 🚀 Quick Start

### Prerequisites

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### Build

```bash
cargo build --release
```

### Run

```bash
./target/release/rustchain-miner-rust --wallet YOUR_WALLET --node https://50.28.86.131
```

### Example

```bash
cargo run -- --wallet RTCb72a1accd46b9ba9f22dbd4b5c6aad5a5831572b
```

---

## 📊 Output

```
🦀 RustChain Miner (Rust Port)
Wallet: RTCb72a1accd46b9ba9f22dbd4b5c6aad5a5831572b
Node: https://50.28.86.131
Threads: 4

📊 Current Epoch: 73
📊 Current Slot: 10554
📊 Active Miners: 12
💰 Balance: 0.00 RTC

⛏️  Starting mining with 4 threads...
```

---

## 📁 Files

- `Cargo.toml` - Dependencies
- `src/main.rs` - Main application

---

## ✅ Progress

- [x] Project structure
- [x] CLI parsing
- [x] Epoch API integration
- [x] Balance API integration
- [ ] Mining logic
- [ ] Testing
- [ ] Submit PR

---

**ETA**: 2 hours
